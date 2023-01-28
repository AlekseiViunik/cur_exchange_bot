import os
import requests
import time

from datetime import date, datetime
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()


EXCHANGE_API_TOKEN = os.getenv("EXCHANGE_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_ID")
ENDPOINT = "https://api.apilayer.com/fixer/latest?base=TRY&symbols=EUR,USD,RUB"
HEADERS = {"apikey": f"{EXCHANGE_API_TOKEN}"}
HOW_OFTEN = 2   # times a day
RETRY_TIME = 3600
SECONDS_IN_DAY = 86400


def get_api_answer():
    """Gets an API answer from endpoint and returns json to parse."""
    response = requests.get(ENDPOINT, headers=HEADERS)
    return response.json()


def check_response(response):
    """Checks response for keys which need us. Returns the same argument which
    have been given or rises an error."""
    if not isinstance(response, dict) or response is None:
        message = "Answer doesn't contain correct data!"
        raise TypeError(message)
    if response.get('date') is None:
        message = "Answer's dictionary doesn't contain the 'date' key!"
        raise KeyError(message)
    if response.get('rates') is None:
        message = "Answer's dictionary doesn't contain the 'rates' key!"
    if response.get('timestamp') is None:
        message = "Answer's dictionary doesn't contain the 'timestamp' key!"
        raise KeyError(message)
    if not isinstance(response.get('rates'), dict):
        message = "'rates' key isn't a dictionary type!"
        raise TypeError(message)
    return response


def parse_response(response):
    """Parses json and returns the message which will be used by bot to
    send it in Telegram."""
    cur_time = response.get("timestamp")
    cur_date = response.get("date")
    cur_rates = response.get("rates")
    usd_rate = cur_rates["USD"]
    eur_rate = cur_rates["EUR"]
    rub_rate = cur_rates["RUB"]
    usd_costs_lira = 1 / usd_rate
    eur_costs_lira = 1 / eur_rate
    message = (
        f"Today ({cur_date}):" 
        f"\n1 USD costs {usd_costs_lira} liras,"
	f"\n1 EUR costs {eur_costs_lira} liras,"
	f"\n1 Lira costs {rub_rate} rubles."
    )
    return message

def check_tokens():
    """Checks for all variables of the environment."""
    return all((
        EXCHANGE_API_TOKEN,
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_CHAT_ID,
    ))


def main():
    last_date_exchange = None
    now_hour = datetime.now().hour
    while True:
        if (
            last_date_exchange != date.today().day and
            now_hour > 9
        ):
            if not check_tokens():
                error_message = (
                    "Requirement variables in .env file are missing! "
                    "The program forcibly stopped!"
                )
                raise NameError(error_message)
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            response = get_api_answer()
            if response:
                response = check_response(response)
                message = parse_response(response)
            bot.send_message(TELEGRAM_CHAT_ID, message)
            last_date_exchange = date.today().day
            time.sleep(SECONDS_IN_DAY // HOW_OFTEN)
            now_hours = datetime.now().hour
            continue
        time.sleep(RETRY_TIME)
        now_hours = datetime.now().hour

if __name__ == '__main__':
    main()
