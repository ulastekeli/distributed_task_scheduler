from client import TaskClient
import random


client = TaskClient("http://localhost:5000")

task_functions = ["mock_ml_task", "mock_cv_task"]
task_types = {
    "mock_ml_task" : ["Random Forest", "Support Vector Machines (SVM)", "K-Means Clustering", "Gradient Boosting", "Principal Component Analysis (PCA)"],
    "mock_cv_task" : ["Object Detection", "Image Segmentation", "Background Subtraction", "Field Registration", "Facial Recognition", "Gender and Age Prediction"]
}

for i in range(55):
    task_function = random.choice(task_functions)
    task_type = random.choice(task_types[task_function])
    mock_ml_task = client.create_task(task_function, random.randint(1,20) * 1000, task_type)
    task_response = client.send_task(mock_ml_task)
    print("Task Submitted:", task_response)