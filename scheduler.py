from flask import Flask, request, jsonify
from threading import Thread
import queue
import defined_functions
import psutil
import GPUtil
from datetime import datetime
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

class TaskScheduler:

    def __init__(self, max_workers, max_task_retries=3):
        self.tasks = {}  
        self.max_workers = max_workers
        self.max_task_retries = max_task_retries
        self.task_status = {}
        self.worker_status = {'busy': 0, 'idle': max_workers}
        self.workers = [Thread(target=self.worker) for _ in range(max_workers)]
        self.task_id_counter = 0
        self.task_queue = queue.Queue()


    def worker(self):
        while True:
            task_id = self.task_queue.get()
            if task_id is None:
                break
            task = self.tasks.get(task_id)
            if task["no_of_processes"] == self.max_task_retries:
                self.remove_task(task_id)
            if task["delete"]:
                self.task_status[task["id"]] = "Canceled"
                continue
            self.worker_status['busy'] += 1
            self.worker_status['idle'] -= 1
            try:
                self.task_status[task_id] = "In Progress"
                self.execute_task(task)
            except:
                self.task_status[task_id] = "On Hold"
                self.add_task(task)
            self.worker_status['busy'] -= 1
            self.worker_status['idle'] += 1
            self.task_queue.task_done()


    def execute_task(self, task):
        function_name = task["function_name"]
        arguments = task["arguments"]
        try:
            task_function = getattr(defined_functions, function_name)
            task["no_of_processes"] += 1
            result = task_function(*arguments)
            self.task_status[task["id"]] = "Completed"
            task["completion_time"] = datetime.now()
            print(result)
        except AttributeError:
            self.task_status[task["id"]] = "Failed: Function not found"
    
    def add_task(self, task_data):
        if "id" in task_data.keys():
            task = task_data
        else:
            task_id = self.task_id_counter
            task = {"id": task_id, "function_name": task_data["function_name"], "arguments": task_data["arguments"], "delete": False, "submission_time": datetime.now(), "completion_time": None, "no_of_processes": 0}
        self.tasks[task_id] = task
        self.task_queue.put(task_id)
        self.task_status[task_id] = "On Hold"
        self.task_id_counter += 1
        return task_id


    def get_task_status(self, task_id):
        return self.task_status.get(task_id, "Unknown")

    def get_monitoring_data(self):
        # CPU usage in percentage
        cpu_usage = psutil.cpu_percent(interval=0.2)

        # RAM usage
        ram = psutil.virtual_memory()
        # ram_allocated = f"{ram.used / (1024**3):.2f} GB"
        ram_allocated = ram.used / (1024**3)
        # ram_total = f"{ram.total / (1024**3):.2f} GB"
        ram_total = ram.total / (1024**3)
        
        ram_usage = f"{ram.percent} %"

        # GPU usage and GPU RAM
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # Assuming a single GPU
            gpu_memory_util = f"{gpu.memoryUtil * 100}%"
            gpu_usage = f"{gpu.load * 100}%"
            gpu_memory_allocated = gpu.memoryUsed
            gpu_memory_total = gpu.memoryTotal
        else:
            gpu_usage = "Not Available"
            gpu_memory_allocated = "Not Available"
            gpu_memory_total = "Not Available"
            gpu_memory_util = "Not Available"

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_usage = f"{disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB ({disk.percent}%)"

        return {
            "CPU": cpu_usage,
            "RAM Allocated": ram_allocated,
            "RAM Total": ram_total,
            "RAM Usage": ram_usage,
            "GPU Usage": gpu_usage,
            "GPU RAM Allocated": gpu_memory_allocated,
            "GPU RAM Total": gpu_memory_total,
            "GPU RAM Usage": gpu_memory_util,
            "Disk": disk_usage,
            "Idle Workers": self.worker_status['idle'],
            "Busy Workers": self.worker_status['busy'],
            "Total Workers": self.max_workers
        }
    
    def get_all_tasks(self):
        # Return a list of all tasks with their details
        return [{"id": task_id, "status": self.task_status.get(task_id, "Unknown"), "arguments": task["arguments"], "task": task["function_name"]}
                for task_id, task in self.tasks.items()]
    
    def remove_task(self, task_id):
        # Logic to remove a task from the queue
        if task_id in self.task_status:
            task = self.tasks.get(task_id)
            task["delete"] = True
            self.task_status[task_id] = "Canceled"
            return True
        return False

    def start(self):
        for worker in self.workers:
            worker.start()

    def stop(self):
        for _ in self.workers:
            self.task_queue.put(None)
        for worker in self.workers:
            worker.join()

scheduler = TaskScheduler(max_workers=5)
scheduler.start()

# Flask endpoint
@app.route('/remove_task/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    print("****"*10)
    print("Deleted task", task_id)
    print("****"*10)
    success = scheduler.remove_task(task_id)
    return jsonify({"success": success})

# Flask endpoint
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    tasks = scheduler.get_all_tasks()
    return jsonify(tasks)

@app.route('/submit_task', methods=['POST'])
def submit_task():
    task_data = request.json
    task_id = scheduler.add_task(task_data)
    return jsonify({"task_id": task_id})

@app.route('/task_status/<int:task_id>', methods=['GET'])
def task_status(task_id):
    status = scheduler.get_task_status(task_id)
    return jsonify({"task_id": task_id, "status": status})

@app.route('/monitoring_data', methods=['GET'])
def monitoring_data():
    data = scheduler.get_monitoring_data()
    return jsonify(data)

def run_scheduler_server():
    app.run(port=5000)

server_thread = Thread(target=run_scheduler_server)
server_thread.start()
