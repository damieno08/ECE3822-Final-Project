/*
text_serializer.cpp - Text serialization implementation

Author: [Student Name]
Date: [Date]
*/

#include "text_serializer.h"

std::string TextSerializer::serialize(const Player& player) {
    std::ostringstream ss;
    ss << player.get_game_name() << "|"
       << player.get_id() << "|"
       << player.get_name() << "|"
       << player.get_x() << "|"
       << player.get_y() << "|"
       << player.get_character_type() << "|"
       << player.get_status();
    return ss.str();
}

Player TextSerializer::deserialize(const std::string& data) {
    std::istringstream ss(data);
    std::string game_name, id_str, name, x_str, y_str, character_type, status;

    std::getline(ss, game_name, '|');
    std::getline(ss, id_str, '|');
    std::getline(ss, name, '|');
    std::getline(ss, x_str, '|');
    std::getline(ss, y_str, '|');
    std::getline(ss, character_type, '|');
    std::getline(ss, status);  // last field, no delimiter needed

    int id = std::stoi(id_str);
    float x = std::stof(x_str);
    float y = std::stof(y_str);

    Player player(game_name, id, name, x, y, -1);  // socket is -1, not transmitted
    player.set_character_type(character_type);
    player.set_status(status);

    return player;
}

std::string TextSerializer::getName() const {
    return "Text";
}