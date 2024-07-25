import os
import subprocess
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    subprocess.run(["streamlit", "run", "app.py"])
