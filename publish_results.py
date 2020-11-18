import logging
import telegram

from constants import PUBLISH_RESULTS_HELLO_MESSAGE, PUBLISH_RESULTS_LINE_TEMPLATE, RESULTS_SUPPORTED_COUNTRIES, \
    POINTS_MAP
from db import get_track_of_the_day
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from utils import parse_leaderboard


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Publish results script started!")

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

        print('-' * 80)
        print('all results:')
        results = []
        for result in new_leaderboard:
            print(result)
            # filter by country
            if result['country'] in RESULTS_SUPPORTED_COUNTRIES:
                results.append(result)

        daily_results = []
        if results:
            print('-' * 80)
            print('filtered results:')
            messages = []
            for num, result in enumerate(results):
                points = POINTS_MAP.get(num+1, 0)
                messages.append(
                    PUBLISH_RESULTS_LINE_TEMPLATE.format(num + 1, result['name'], result['time'], points, result['position']))
                daily_results.append({
                    'position': num + 1,
                    'name': result['name'],
                    'points': points
                })

            message = '\n\n'.join(messages)
            message = PUBLISH_RESULTS_HELLO_MESSAGE + '\n\n' + message + '\n\n\n' + saved_track[3]  # add URL
            bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
            logging.info("Results published")
        else:
            logging.info("No records!")
            print('No records!')

        if daily_results:
            # TODO save daily results
            """"""

    except Exception as error:
        logging.exception(error)
        print('Uncaught error: ')
        print(error)
        import traceback
        traceback.print_exc()
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in publish_results: ' + str(error),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
