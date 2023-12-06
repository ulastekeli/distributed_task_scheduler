from client import TaskClient
import json

client = TaskClient("http://localhost:5000")
monitoring_data = client.request_all_task_data()
print("Task Data")
for item in monitoring_data:
    print(item)