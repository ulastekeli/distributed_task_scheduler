import requests

class TaskClient:
    def __init__(self, scheduler_url):
        self.scheduler_url = scheduler_url

    def create_task(self, function_name, *args):
        # This method will create a task with the specified function name and arguments
        return {"function_name": function_name, "arguments": args}

    def send_task(self, task):
        # Sending a task to the scheduler via HTTP POST request
        response = requests.post(f"{self.scheduler_url}/submit_task", json=task)
        return response.json()

    def request_task_status(self, task_id):
        # Requesting the status of a task via HTTP GET request
        response = requests.get(f"{self.scheduler_url}/task_status/{task_id}")
        return response.json()

    def request_monitoring_data(self):
        # Requesting resource monitoring data via HTTP GET request
        response = requests.get(f"{self.scheduler_url}/monitoring_data")
        return response.json()

    def request_all_task_data(self):
        # Requesting resource monitoring data via HTTP GET request
        response = requests.get(f"{self.scheduler_url}/get_tasks")
        return response.json()

