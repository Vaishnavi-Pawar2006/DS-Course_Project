# custom_queue.py

class CustomQueue:
    """A robust, linked-list implementation of a FIFO queue."""

    # Inner class for the nodes, similar to the C++ struct Node
    class _Node:
        """A node in the linked list queue."""
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        """Initializes an empty queue."""
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, val):
        """Adds a value to the rear of the queue."""
        new_node = self._Node(val)
        if self.rear:
            self.rear.next = new_node
        else:
            # If the queue is empty, the new node is both front and rear
            self.front = new_node
        self.rear = new_node
        self._size += 1

    def dequeue(self):
        """
        Removes and returns the value from the front of the queue.
        Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue!")

        val = self.front.data
        self.front = self.front.next
        if not self.front:
            # If the queue becomes empty, update rear as well
            self.rear = None
        self._size -= 1
        return val

    def peek(self):
        """
        Returns the value at the front of the queue without removing it.
        Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek into an empty queue!")
        return self.front.data

    def is_empty(self) -> bool:
        """Returns True if the queue is empty, False otherwise."""
        return self._size == 0

    def get_size(self) -> int:
        """Returns the number of elements in the queue."""
        return self._size
        
    def __len__(self) -> int:
        """Allows using len(queue) to get the size."""
        return self._size