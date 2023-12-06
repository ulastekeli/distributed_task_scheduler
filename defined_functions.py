# defined_tasks.py
import time
import random

def mock_ml_task(data_size, model_type):
    print(f"Simulating ML task: Training a {model_type} model with {data_size} data points.")
    time.sleep(random.randint(0,15))    
    # Placeholder for ML training logic
    return f"ML Task Completed: {model_type} model trained with {data_size} data points."

def mock_cv_task(image_count, process_type):
    print(f"Simulating CV task: Processing {image_count} images with {process_type}.")
    time.sleep(random.randint(0,15))
    # Placeholder for CV processing logic
    return f"CV Task Completed: Processed {image_count} images using {process_type}."
