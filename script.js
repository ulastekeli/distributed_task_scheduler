// Track the currently selected task ID
let selectedTaskId = null;

// Chart data storage and counters
let ramChartData, cpuChartData, workerChartData, diskChartData;
let dataCounter = 0;

// Utility functions
function createTaskItem(task) {
    const isTaskSelected = task.id === selectedTaskId;
    return `
        <div class="task-item" data-task-id="${task.id}">
            <div>ID: ${task.id}</div>
            <div>Status: ${task.status}</div>
            <div>Arguments: ${JSON.stringify(task.arguments)}</div>
            <div>Task: ${task.task}</div>
            <button class="cancel-task-btn" data-task-id="${task.id}" style="${isTaskSelected ? '' : 'display: none;'}">Cancel Task</button>
        </div>
    `;
}

// API interactions
function fetchTasks() {
    axios.get('http://localhost:5000/get_tasks')
        .then(response => {
            const tasks = response.data;
            const list = document.getElementById('task-list');
            list.innerHTML = tasks.map(createTaskItem).join('');
            if (selectedTaskId) {
                const selectedTaskElement = list.querySelector(`[data-task-id='${selectedTaskId}'] .cancel-task-btn`);
                if (selectedTaskElement) {
                    selectedTaskElement.style.display = 'block';
                }
            }
        })
        .catch(error => console.error('Error fetching tasks:', error));
}

function cancelTask(taskId) {
    axios.delete(`http://localhost:5000/remove_task/${taskId}`)
        .then(response => {
            console.log('Task cancelled:', response.data);
            selectedTaskId = null;
            fetchTasks();
        })
        .catch(error => console.error('Error cancelling task:', error));
}

// Event Listeners
document.getElementById('task-list').addEventListener('click', function(event) {
    let targetElement = event.target;
    while (targetElement != null) {
        if (targetElement.className.includes('task-item')) {
            const taskId = targetElement.dataset.taskId;
            selectedTaskId = taskId;
            fetchTasks();
            return;
        } else if (targetElement.className.includes('cancel-task-btn')) {
            const taskId = targetElement.dataset.taskId;
            cancelTask(taskId);
            return;
        }
        targetElement = targetElement.parentElement;
    }
});

// Initialize charts
function initializeCharts() {
    const ramCtx = document.getElementById('ramChart').getContext('2d');
    const cpuCtx = document.getElementById('cpuChart').getContext('2d');
    const workerCtx = document.getElementById('workerChart').getContext('2d');
    const diskCtx = document.getElementById('diskChart').getContext('2d');

    ramChartData = new Chart(ramCtx, createChartConfig('RAM Allocated', 'RAM Total'));
    cpuChartData = new Chart(cpuCtx, createChartConfig('CPU'));
    workerChartData = new Chart(workerCtx, createChartConfig('Idle Workers', 'Busy Workers'));
    diskChartData = new Chart(diskCtx, createChartConfig('Disk'));
}

// Create chart configuration
function createChartConfig(...labels) {
    return {
        type: 'line',
        data: {
            labels: [],
            datasets: labels.map((label, index) => ({
                label: label,
                data: [],
                borderColor: ['blue', 'green', 'red', 'orange', 'purple', 'cyan'][index],
                fill: false
            }))
        },
        options: {
            scales: {
                xAxes: [{ ticks: { autoSkip: true, maxTicksLimit: 20 } }],
                yAxes: [{ ticks: { beginAtZero: true } }]
            }
        }
    };
}

// Fetch monitoring data
function fetchMonitoringData() {
    axios.get('http://localhost:5000/monitoring_data')
        .then(response => {
            const data = response.data;

            // Update charts
            updateChartData(ramChartData, [data['RAM Allocated'], data['RAM Total']]);
            updateChartData(cpuChartData, [data['CPU']]);
            updateChartData(workerChartData, [data['Idle Workers'], data['Busy Workers']]);
            updateChartData(diskChartData, [data['Disk']]);

            // Increment data counter
            dataCounter++;
        })
        .catch(error => console.error('Error fetching monitoring data:', error));
}

// Update Chart Data
function updateChartData(chart, values) {
    chart.data.labels.push(dataCounter);
    values.forEach((value, index) => {
        chart.data.datasets[index].data.push(value);
        if (chart.data.datasets[index].data.length > 300) {
            chart.data.datasets[index].data.shift();
        }
    });

    if (chart.data.labels.length > 300) {
        chart.data.labels.shift();
    }

    chart.update();
}

// Event Listeners and Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    fetchTasks();
    initializeCharts();
    setInterval(fetchTasks, 2000);
    setInterval(fetchMonitoringData, 2000);
});
