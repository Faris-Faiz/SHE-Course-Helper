import time
import subprocess
from datetime import datetime

def main():
    while 1:
        time_format = "%Y%m%d%H%M"
        now = datetime.now().strftime(time_format)

        filename = f"{now}.xlsx"

        subprocess.run(['venv/Scripts/python.exe', 'mayascrape2.py', filename])

        #subprocess.run(['venv/Scripts/python.exe', 'shecoursefilter.py', filename])

        time.sleep(60*60)  # an hour

if __name__ == '__main__':
    main()
