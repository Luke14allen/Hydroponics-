import pandas as pd
from PIL import Image
import numpy as np
import os

def process_csv(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Example: Extract specific columns like temperature, humidity
    relevant_data = data[['temperature', 'humidity']]
    
    # Clean data (e.g., handle missing values)
    relevant_data = relevant_data.dropna()  # Removing rows with missing values
    
    # Perform further processing, e.g., averaging sensor readings
    avg_temp = relevant_data['temperature'].mean()
    avg_humidity = relevant_data['humidity'].mean()

    return avg_temp, avg_humidity


def process_image(file_path):
    # Open and preprocess the image
    image = Image.open(file_path)
    image = image.resize((224, 224))  # Resize for model input, e.g., for CNN
    image_array = np.array(image) / 255.0  # Normalize pixel values
    
    # If needed, add batch dimension for model input (e.g., for TensorFlow)
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


def format_data_for_dashboard(avg_temp, avg_humidity):
    dashboard_data = {
        "temperature": f"{avg_temp:.2f} °C",
        "humidity": f"{avg_humidity:.2f} %"
    }
    return dashboard_data

file_path = os.path.join(os.getcwd(), 'sensor_data.csv')
print("Looking for file:", file_path)
avg_temp, avg_humidity = process_csv(file_path)

print(format_data_for_dashboard(avg_temp, avg_humidity))

# Test image processing
processed_image = process_image('sample_image.jpg')
print("Image processed:", processed_image.shape)
print(f"Looking for file: {sensor_data.csv}")
