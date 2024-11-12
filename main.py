import detector
import app
import subprocess

def main():
    app.runApp()
    subprocess.run(["python","detector.py"])

if __name__ == "__main__":
    main()  