import logging
import telegram

from constants import PUBLISH_RESULTS_HELLO_MESSAGE, PUBLISH_RESULTS_TRACK_NAME, \
    PUBLISH_RESULTS_LINE_TEMPLATE, RESULTS_SUPPORTED_COUNTRIES, POINTS_MAP, PUBLISH_RESULTS_TAG, PATRONS_LIST, \
    PATRONS_TEXT
from db import get_track_of_the_day, save_daily_results
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID, DB_TABLE_PREFIX
from utils import parse_leaderboard


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Publish results script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    logging.debug(bot)

    try:

        saved_track = get_track_of_the_day()
        logging.debug('-' * 80)
        logging.debug('Track of the day: ' + str(saved_track))

        new_leaderboard = parse_leaderboard(saved_track)
        logging.debug('-' * 80)
        logging.debug('new_leaderboard:')
        logging.debug(new_leaderboard)

        logging.debug('-' * 80)
        logging.debug('all results:')
        results = []
        for result in new_leaderboard:
            logging.debug(result)
            # filter by country
            if result['country'] in RESULTS_SUPPORTED_COUNTRIES:
                results.append(result)

        # mock for testing
        if DB_TABLE_PREFIX and DB_TABLE_PREFIX.startswith('test'):
            results = [
                {
                    'position': '0',
                    'time': '29.5',
                    'name': 'TEST1',
                    'country': 'Ukraine',
                    'ranking': '',
                    'model': '',
                    'date': '',
                    'version': '1.16',
                },
                {
                    'position': '2',
                    'time': '31.5',
                    'name': 'TEST2',
                    'country': 'Ukraine',
                    'ranking': '',
                    'model': '',
                    'date': '',
                    'version': '',
                }
            ]

        daily_results = []
        if results:
            logging.debug('-' * 80)
            logging.debug('filtered results:')
            messages = []
            for num, result in enumerate(results):
                points = POINTS_MAP.get(num+1, 1)   # as requested, everybody gets at least 1
                messages.append(
                    PUBLISH_RESULTS_LINE_TEMPLATE.format(num + 1, result['name'], result['time'], points, result['position']))
                daily_results.append({
                    'position': num + 1,
                    'name': result['name'],
                    'points': points
                })

            message = '\n\n'.join(messages)
            message = PUBLISH_RESULTS_HELLO_MESSAGE + '\n' + \
                      PUBLISH_RESULTS_TRACK_NAME.format(saved_track[1] + ' - ' + saved_track[2]) + \
                      '\n\n\n' + message + '\n\n' + PUBLISH_RESULTS_TAG + '\n\n'
            patreons_list = ', '.join(PATRONS_LIST)
            patreons_text = PATRONS_TEXT.format(patreons_list)
            message = message + patreons_text + '\n\n'
            bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)
            logging.info("Results published")

            if daily_results:
                save_daily_results(daily_results)

        else:
            logging.info("No records!")
            logging.debug('No records!')

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        logging.debug(error)
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in publish_results: ' + str(exc),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
