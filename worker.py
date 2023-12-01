import uuid
import traceback

class Worker:
    def __init__(self):
        """
        Initialize a worker with a unique ID and set it as available.
        """
        self.worker_id = str(uuid.uuid4())
        self.available = True

    def run(self, task, callback=None):
        """
        Execute a given task and handle any potential failures.
        
        :param task: The Task object to be executed.
        :param callback: Optional callback function to report task status.
        """
        if self.available:
            self.available = False
            try:
                result = task.execute()
                status = "Success"
                return result
            except Exception as e:
                print(f"Error in worker {self.worker_id}: {traceback.format_exc()}")
                status = "Failed"
                return None
            finally:
                self.available = True
                if callback:
                    callback(task, status)
        else:
            print(f"Worker {self.worker_id} is currently busy.")
            if callback:
                callback(task, "Busy")
            return None

