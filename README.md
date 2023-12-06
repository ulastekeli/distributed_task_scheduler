# Distributed Task Scheduler

This project is a python implementation of a distributed task scheduler application that uses native python threads and queues to showcase such system. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

To build and run the project, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/ulastekeli/distributed_task_scheduler.git
```
2. Create a virtual environment and install requirements

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

The project provides a distributed task scheduler that allows you to submit, monitor, and manage tasks. The main components of the project are:

### Task Scheduler

The `TaskScheduler` class is responsible for managing tasks and worker threads. It allows you to:

- Add tasks to the scheduler.
- Monitor the status of tasks.
- Remove tasks from the queue.
- Obtain monitoring data on system resource usage (CPU, RAM, GPU, Disk).
- Retrieve a list of all tasks with their details.

### Starting the Scheduler

To start the task scheduler server, simply run the scheduler script:

```bash
python scheduler.py
```

The server will run on port 5000, and you can access the project's dashboard by opening index.html in a web browser.

### Example Scripts

The project includes three example scripts to demonstrate its functionality:

- `send_task_request.py`: Creates and sends a number of mock tasks to the scheduler.
- `send_monitoring_request.py`: Creates and sends a monitoring request and prints the response.
- `send_status_request.py`: Creates and sends a request that receives all tasks with their status information.

You can run these scripts to interact with the task scheduler and observe its behavior.

### Dashboard
The project includes an index.html file that acts as a dashboard. You can open this file in a web browser to visualize and interact with the task scheduler's status and monitoring data.