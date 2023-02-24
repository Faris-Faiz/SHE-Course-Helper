## How to use

create a `.env` file in the mayascrapingproject folder and inside it, write this, and don't forget to remove the square brackets.

```bash
user=[YOUR MAYA USERNAME]
pass=[YOUR MAYA PASSWORD]
```

then create virtual environment like so

`python -m venv venv`

NOTE: the virtual environment folder really need to be named `venv`, if you want to change, change stuff in [cron.py](./cron.py)

after creating virtual environment, activate the environment and install the requirements by runnning

`pip install -r keperluan.txt`

then, run `python cron.py` inside the environment then it shall run the scraper every hour


IMPORTANT NOTES
---
_CAUTION: DO NOT TURN OFF YOUR MONITOR OR LET IT BE TURNED OFF, IT WILL DISTURB THE SCRAPING PROCESS_


To enter the virtual environment, tekan v sekali then tab, s sekali then tab, and a tekan tiga kali, bukan dua kali until you see Activate.ps1 (.com)


NOTE: If this is your first time running a virtual environment, on Windows, you need to run terminal as an admin, and execute the following command:

`set-executionpolicy RemoteSigned -Scope CurrentUser`
