import subprocess

def main():
    # Run app.py
    app_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Run detector.py
    detector_process = subprocess.Popen(["python", "detector.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Wait for the processes to complete
        app_stdout, app_stderr = app_process.communicate()
        detector_stdout, detector_stderr = detector_process.communicate()

        # Print outputs (optional)
        print("Output from app.py:")
        print(app_stdout.decode())
        print("Errors from app.py (if any):")
        print(app_stderr.decode())
        
        print("\nOutput from detector.py:")
        print(detector_stdout.decode())
        print("Errors from detector.py (if any):")
        print(detector_stderr.decode())
    
    except KeyboardInterrupt:
        # Terminate processes on keyboard interrupt
        app_process.terminate()
        detector_process.terminate()
        print("\nProcesses terminated.")

if __name__ == "__main__":
    main()