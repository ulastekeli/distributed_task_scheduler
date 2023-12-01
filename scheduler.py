from task_queue import TaskQueue

class Scheduler:
    def __init__(self, scaling_manager):
        """
        Initialize the Scheduler with a reference to the Scaling Manager.

        :param scaling_manager: The ScalingManager instance for managing worker scaling.
        """
        self.task_queue = TaskQueue()
        self.scaling_manager = scaling_manager
        self.active_workers = []  # List to keep track of active workers

    def schedule(self):
        """
        Continuously assign tasks from the queue to available workers.
        """
        while True:
            if not self.task_queue.is_empty():
                task = self.task_queue.dequeue()
                available_worker = self.scaling_manager.get_available_worker()
                if available_worker:
                    available_worker.run(task, self.task_completion_handler)
                else:
                    # Re-enqueue the task if no workers are available
                    self.task_queue.enqueue(task)

    def handle_failed_task(self, task):
        """
        Handle a failed task, potentially re-queuing it for another attempt.

        :param task: The failed Task object.
        """
        # This can be expanded based on how you want to handle task retries
        self.task_queue.enqueue(task)

    def task_completion_handler(self, task, status):
        """
        Handle the completion of a task, including failures.

        :param task: The Task object.
        :param status: The execution status of the task.
        """
        if status == "Failed":
            self.handle_failed_task(task)
