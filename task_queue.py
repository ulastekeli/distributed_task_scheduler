from queue import Queue

class TaskQueue:
    def __init__(self):
        """
        Initialize an empty task queue.
        """
        self.queue = Queue()

    def enqueue(self, task):
        """
        Add a new task to the queue.
        
        :param task: The Task object to be added to the queue.
        """
        self.queue.put(task)

    def dequeue(self):
        """
        Remove and return the next task from the queue.
        
        :return: The next Task object from the queue.
        """
        if not self.queue.empty():
            return self.queue.get()
        return None

    def is_empty(self):
        """
        Check if the queue is empty.
        
        :return: True if the queue is empty, False otherwise.
        """
        return self.queue.empty()
