
import sys

sys.path.append('../')


class linked_list:

    def __init__(self):
        self.current_node = None
        self.head = None
        self.tail = None

    def add_node(self, node):
        """
        This function will add a new node to the end of our linked list.

        Node: a node object that will be added to the list
        
        Function will return true on success and false on failure

        """
        if type(node) != "class 'datastructures.node.node'":
            return False
        
        # check if list has any nodes and make head node if not
        if self.head == None:
            self.head = node
            self.forward = self.head
            self.tail = node
            self.current_node = self.head
            return True
        
        # update tail and pointers for nodes
        self.tail.next = node
        node.last = self.tail
        self.tail = node
        self.backward = self.tail
        node.next = None

        return True

    def move(self, dir="forward"):

        if self.current_node == None:
            return False

        if dir == "forward":
            
            self.current_node = self.current_node.next

        elif dir == "backward":
            self.current_node = self.current_node.last
        

class node:
    def __init__(self):
        self.next = None
        self.last = None
        self.val = None
        