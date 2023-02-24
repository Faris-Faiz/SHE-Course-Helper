## How to use

create a `.env` file and inside write this

```bash
user=[YOUR MAYA USERNAME]
pass=[YOUR MAYA PASSWORD]
```

then create virtual environment like so

`python -m venv venv`

NOTE: the virtual environment folder really need to be named `venv`, if you want to change, change stuff in [cron.py](./cron.py)

after creating virtual environment, activate the environment and install the requirements by runnning

`pip install -r requirements.txt`

then, run `python cron.py` inside the environment then it shall run the scraper every hour