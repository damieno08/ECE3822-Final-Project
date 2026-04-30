#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>

#include "player.h"
#include "serializer.h"
#include "text_serializer.h"
#include "json_serializer.h"
#include "binary_serializer.h"

#ifdef USE_JSON
    #define SERIALIZER_TYPE JSONSerializer
#elif defined(USE_BINARY)
    #define SERIALIZER_TYPE BinarySerializer
#else
    #define SERIALIZER_TYPE TextSerializer
#endif

class GameServer {
private:
    int server_socket;
    Serializer* serializer;
    int next_player_id = 1;
    int port;

    std::map<std::string, std::map<int, Player*>> game_rooms;

public:
    GameServer(int port)
        : port(port)
    {
        serializer = new SERIALIZER_TYPE();

        server_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (server_socket < 0) {
            std::cerr << "Failed to create socket\n";
            exit(1);
        }

        int opt = 1;
        setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

        struct sockaddr_in address;
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(port);

        if (bind(server_socket, (struct sockaddr*)&address, sizeof(address)) < 0) {
            std::cerr << "Bind failed\n";
            exit(1);
        }

        if (listen(server_socket, 10) < 0) {
            std::cerr << "Listen failed\n";
            exit(1);
        }

        fcntl(server_socket, F_SETFL, O_NONBLOCK);

        std::cout << "Server running on port " << port << "\n";
    }

    ~GameServer() {
        for (auto& room : game_rooms) {
            for (auto& pair : room.second) {
                delete pair.second;
            }
        }
        delete serializer;
        close(server_socket);
    }

    void accept_connections() {
        struct sockaddr_in client_addr;
        socklen_t addr_len = sizeof(client_addr);

        int client_socket = accept(server_socket, (struct sockaddr*)&client_addr, &addr_len);
        if (client_socket < 0) return;  // No pending connections (EAGAIN), that's fine

        std::cout << "[ACCEPT] new socket: " << client_socket << "\n";

        // Read JOIN while socket is still BLOCKING so recv waits for data
        char buffer[1024];
        int n = recv(client_socket, buffer, sizeof(buffer)-1, 0);

        if (n <= 0) {
            close(client_socket);
            return;
        }

        buffer[n] = '\0';
        std::string msg(buffer);

        // Expect: JOIN|GameName|PlayerName
        std::istringstream ss(msg);
        std::string type, game_name, player_name;

        std::getline(ss, type, '|');
        std::getline(ss, game_name, '|');
        std::getline(ss, player_name);

        // Strip trailing newline if present
        if (!player_name.empty() && player_name.back() == '\n')
            player_name.pop_back();

        if (type != "JOIN") {
            std::cerr << "[REJECT] Expected JOIN, got: " << type << "\n";
            close(client_socket);
            return;
        }

        int player_id = next_player_id++;

        Player* p = new Player(
            game_name,
            player_id,
            player_name.empty() ? ("Player" + std::to_string(player_id)) : player_name,
            400.0f,
            300.0f,
            client_socket
        );

        // NOW set non-blocking, after the handshake is complete
        fcntl(client_socket, F_SETFL, O_NONBLOCK);

        game_rooms[game_name][player_id] = p;

        std::cout << "[JOIN] " << player_name << " joined " << game_name << "\n";

        std::string welcome = "CONNECTED|" + std::to_string(player_id) + "\n";
        send(client_socket, welcome.c_str(), welcome.length(), 0);
    }

    void receive_messages() {
        std::vector<int> disconnected;

        for (auto& room_pair : game_rooms) {
            auto& room = room_pair.second;

            for (auto& player_pair : room) {
                Player* p = player_pair.second;
                int sock = p->get_socket();

                char buffer[4096];
                int n = recv(sock, buffer, sizeof(buffer) - 1, 0);

                if (n > 0) {
                    buffer[n] = '\0';
                    std::string msg(buffer);

                    std::istringstream ss(msg);
                    std::string type;
                    std::getline(ss, type, '|');

                    if (type == "UPDATE") {
                        std::string id_str, x_str, y_str, name, character_type, status, game_name;

                        std::getline(ss, id_str, '|');
                        std::getline(ss, x_str, '|');
                        std::getline(ss, y_str, '|');
                        std::getline(ss, name, '|');
                        std::getline(ss, character_type, '|');
                        std::getline(ss, status, '|');
                        std::getline(ss, game_name);

                        // Strip trailing newline
                        if (!game_name.empty() && game_name.back() == '\n')
                            game_name.pop_back();

                        try {
                            if (!x_str.empty() && !y_str.empty()) {
                                float new_x = std::stof(x_str);
                                float new_y = std::stof(y_str);
                                p->set_position(new_x, new_y);
                            }

                            if (!name.empty()) p->set_name(name);
                            if (!character_type.empty()) p->set_character_type(character_type);
                            if (!status.empty()) p->set_status(status);
                            if (!game_name.empty()) p->set_game_name(game_name);

                        } catch (...) {
                            std::cerr << "[ERROR] Bad UPDATE from Player " << p->get_id() << "\n";
                        }
                    }
                    else if (type == "CONNECT") {
                        std::string name, character_type, game_name;

                        std::getline(ss, name, '|');
                        std::getline(ss, character_type, '|');
                        std::getline(ss, game_name);

                        if (!name.empty()) p->set_name(name);
                        if (!character_type.empty()) p->set_character_type(character_type);
                        if (!game_name.empty()) p->set_game_name(game_name);
                    }
                }
                else if (n == 0 || (n < 0 && errno != EAGAIN && errno != EWOULDBLOCK)) {
                    disconnected.push_back(sock);
                }
            }
        }

        for (int sock : disconnected) {
            for (auto& room_pair : game_rooms) {
                auto& room = room_pair.second;
                for (auto it = room.begin(); it != room.end(); ) {
                    if (it->second->get_socket() == sock) {
                        std::cout << "[DISCONNECT] Player " << it->second->get_id()
                                  << " (" << it->second->get_name() << ") left "
                                  << room_pair.first << "\n";
                        close(sock);
                        delete it->second;
                        it = room.erase(it);
                    } else {
                        ++it;
                    }
                }
            }
        }
    }

    void broadcast_state() {
        for (auto& room_pair : game_rooms) {
            auto& room = room_pair.second;

            for (auto& receiver_pair : room) {
                Player* receiver = receiver_pair.second;

                std::ostringstream state;
                state << "STATE\n";

                for (auto& sender_pair : room) {
                    Player* p = sender_pair.second;
                    state << serializer->serialize(*p) << "\n";
                }

                state << "END\n";

                std::string msg = state.str();
                send(receiver->get_socket(), msg.c_str(), msg.length(), 0);
            }
        }
    }

    void run() {
        std::cout << "Running...\n";

        while (true) {
            accept_connections();
            receive_messages();
            broadcast_state();
            usleep(16666);
        }
    }
};

int main(int argc, char* argv[]) {
    int port = 8080;

    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if ((arg == "--port" || arg == "-p") && i + 1 < argc) {
            port = atoi(argv[++i]);
        }
    }

    GameServer server(port);
    server.run();
}