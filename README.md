# cur_exchange_bot
![Python version](https://img.shields.io/badge/python-3.7-yellow)

```sh
Bot, which shows the Lira's currency exchange in telegram. It takes data from fixer.io.
You can choose how many times a day it shows
```

## Running project

Clone repository. Install and activate virtual environment.

```
$ python3 -m venv venv

- For Mac or Linux:
$ source venv/bin/activate

- For Windows
$ source venv/Scripts/activate 
``` 

Install dependencies  from requirements.txt.

```
pip install -r requirements.txt
``` 
If you need to set, how many times a day you want recieve a message,
you can open exchange.py and set the value 'HOW_OFTEN'.

Also you need to create an .env file and add to it such values as:



Run the project.

```
python3 exchange.py
``` 
