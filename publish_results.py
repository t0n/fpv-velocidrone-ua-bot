import telegram
from telegram import ParseMode

from constants import PUBLISH_RESULTS_HELLO_MESSAGE, PUBLISH_RESULTS_LINE_TEMPLATE, RESULTS_SUPPORTED_COUNTRIES
from db import get_track_of_the_day
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from utils import parse_leaderboard


def main():
    print("Leaderboard updates script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    print(bot)

    try:

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
            if result['country'] in RESULTS_SUPPORTED_COUNTRIES:
                results.append(result)

        if results:
            messages = []
            for num, result in enumerate(results):
                messages.append(
                    PUBLISH_RESULTS_LINE_TEMPLATE.format(num + 1, result['name'], result['time'], result['position']))

            message = '\n\n'.join(messages)
            message = PUBLISH_RESULTS_HELLO_MESSAGE + '\n\n' + message + '\n\n\n' + saved_track[3]  # add URL
            bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=ParseMode.HTML)
        else:
            print('No records!')

    except Exception as error:
        print('Uncaught error: ')
        print(error)
        import traceback
        traceback.print_exc()
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text='⚠️ @antonkoba Error in publish_results: ' + str(error), parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    main()
