import csv
import os
from datetime import datetime
from PIL import Image

def run():
    #Path to your CSV file and images directory pip install pillow 
    current_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(current_dir, "data", "sensor_data.csv")
    images_folder_path = os.path.join(current_dir, "images")


    #unction to read CSV and get rows by date
    def read_csv_by_date(csv_file_path):
        data_by_date = {}
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                
                date = row.get('date_time')  # Change 'date' to the actual column name
                if date:
                    data_by_date[date] = row
        return data_by_date

    #Function to extract date from images using OCR
    def extract_date_from_image(image_path):
        filename = os.path.basename(image_path)
        # Try to extract date assuming it's in a 'YYYY-MM-DD' format
        try:
            date = datetime.strptime(filename[6:16], '%Y-%m-%d').date()
            return date
        except ValueError:
            pass
        return None

    #Main function to match CSV data with images by date
    def match_csv_with_images(csv_data, images_folder_path):
        matched_data = []
        for image_file in os.listdir(images_folder_path):
            image_path = os.path.join(images_folder_path, image_file)
            image_date = extract_date_from_image(image_path)

            if image_date:
                image_date_str = image_date.strftime('%Y-%m-%d')
                if image_date_str in csv_data:
                    matched_data.append({
                        "image": image_file,
                        "data": csv_data[image_date_str]
                    })
        return matched_data


    csv_data = read_csv_by_date(csv_file_path)

    def getAverages(csv_data):

        total_ph = total_ec = total_ppm = total_temp = total_humidity = 0
        num_rows = len(csv_data)
        for row in csv_data.values():
            total_ph += float(row[' pH'])
            total_ec += float(row['EC'])
            total_ppm += float(row['PPM'])
            total_temp += float(row['Temp'])
            total_humidity += float(row['Humidity'])
        
        average_ph = total_ph / num_rows
        average_ec = total_ec / num_rows
        average_ppm = total_ppm / num_rows
        average_temp = total_temp / num_rows
        average_humidity = total_humidity / num_rows

        Averages = {
            'Average pH': average_ph,
            'Average EC': average_ec,
            'Average PPM': average_ppm,
            'Average Temperature': average_temp,
            'Average Humidity': average_humidity
        }
        return Averages

    def process_images_in_folder(images_folder_path):
        image_dates = {}
        for image_file in os.listdir(images_folder_path):
            # Only process image files (e.g., .jpg, .png)
            if image_file.lower().endswith(('.jpg', '.png')):
                image_path = os.path.join(images_folder_path, image_file)
                date = extract_date_from_image(image_path)
                if date:
                    image_dates[image_file] = date
                else:
                    print(f"No valid date found in filename: {image_file}")
        return image_dates
    image_dates = process_images_in_folder(images_folder_path)
