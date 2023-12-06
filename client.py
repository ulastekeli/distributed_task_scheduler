# Updating client.py to send function names and arguments to the scheduler

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

# Example usage
# client = TaskClient("http://localhost:5000")
# mock_ml_task = client.create_task("mock_ml_task", 100, "logistic_regression")
# task_response = client.send_task(mock_ml_task)
# print("Task Submitted:", task_response)
# mock_ml_task = client.create_task("mock_cv_task", 10, "neural_network")
# task_response = client.send_task(mock_ml_task)
# print("Task Submitted:", task_response)
# mock_ml_task = client.create_task("mock_ml_task", 1200, "clustering")
# task_response = client.send_task(mock_ml_task)
# print("Task Submitted:", task_response)

# task_status = client.request_task_status(58)
# print("Task Status:", task_status)


# This client now creates tasks specifying the function name and its arguments, then sends them to the scheduler.
# Next, we'll update the scheduler to handle these tasks by executing the corresponding functions from defined_tasks.py.
