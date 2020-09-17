from _decimal import Decimal

import telegram
from telegram import ParseMode

from db import get_track_of_the_day
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from update_leaderboard import parse_leaderboard

LEADERBOARD_HELLO_MESSAGE = '🇺🇦🇺🇦🇺🇦 Результати 🇺🇦🇺🇦🇺🇦'  # with UA flag emojis
LEADERBOARD_UPDATE_MESSAGE = '<b></b> - <b>{}</b> - {}'


SUPPORTED_COUNTRIES = [
    'Ukraine',
]


def main():
    print("Leaderboard updates script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    print(bot)

    saved_track = get_track_of_the_day()
    print('-' * 80)
    print('Track of the day: ' + str(saved_track))

    new_leaderboard = parse_leaderboard(saved_track)
    print('-' * 80)
    print('new_leaderboard:')
    print(new_leaderboard)

    results = []
    for result in new_leaderboard:
        print(result)
        # filter by country
        if result['country'] in SUPPORTED_COUNTRIES:
            results.append(result)

    if results:
        messages = []
        for num, result in enumerate(results):
            messages.append(LEADERBOARD_UPDATE_MESSAGE.format(num, result['name'], result['time']))

        message = '\n\n'.join(messages)
        message = LEADERBOARD_HELLO_MESSAGE + '\n---\n\n' + message + '\n\n\n' + saved_track[3]  # add URL
        print('-' * 80)
        print('message: ' + str(message))
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=ParseMode.HTML)
    else:
        print('No records!')


if __name__ == "__main__":
    main()
