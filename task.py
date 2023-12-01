class Task:
    def __init__(self, task_id, function, *args, **kwargs):
        """
        Initialize a new task with a unique ID, the function to be executed,
        and any arguments it requires.
        
        :param task_id: A unique identifier for the task.
        :param function: The function that represents the task's action.
        :param args: Non-keyword arguments for the function.
        :param kwargs: Keyword arguments for the function.
        """
        self.task_id = task_id
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        """
        Execute the task's function with the provided arguments.
        
        :return: The result of the function execution.
        """
        try:
            result = self.function(*self.args, **self.kwargs)
            return result
        except Exception as e:
            # In a real-world scenario, you might want to handle specific exceptions
            # more gracefully or log them.
            print(f"An error occurred while executing task {self.task_id}: {e}")
            return None
