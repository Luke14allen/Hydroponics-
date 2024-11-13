import concurrent.futures
import subprocess

# Function to run app.py (Tkinter GUI)
def run_app():
    subprocess.run(['python3', 'app.py'])

# Function to run detector.py (Flask server)
def run_detector():
    subprocess.run(['python3', 'detector.py'])

if __name__ == '__main__':
    # Use concurrent futures to run both functions concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(run_app)
        executor.submit(run_detector)
