from datastructures.stack import Stack

class History:

    #initialize history class
    def __init__(self):

        # history is a Stack
        self._history = Stack()

    def get_history(self, idx = -1):
        return self._history.peek(idx)

    def set_history(self, session):
        self._history.push(session)


