from client import TaskClient


client = TaskClient("http://localhost:5000")
monitoring_data = client.request_monitoring_data()
print("Monitoring Data:", monitoring_data)