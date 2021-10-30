import logging
import telegram

from constants import PUBLISH_RESULTS_HELLO_MESSAGE, PUBLISH_RESULTS_LINE_TEMPLATE, RESULTS_SUPPORTED_COUNTRIES, \
    POINTS_MAP, RECRAWL_RESULTS_HELLO_MESSAGE
from db import get_track_of_the_day, save_daily_results, save_daily_results_for_day, get_all_daily_results
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from utils import parse_leaderboard


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Publish results script started!")

    # bot = telegram.Bot(TELEGRAM_KEY)
    # logging.debug(bot)

    try:

        saved_track = ('-1', 'Dynamic Weather', 'VOC S1 race1', 'https://www.velocidrone.com/leaderboard/33/467/1.16')  # | ID | NAME | ??? | URL
        logging.debug('-' * 80)
        logging.debug('Track of the day: ' + str(saved_track))

        new_leaderboard = parse_leaderboard(saved_track)
        logging.debug('-' * 80)
        logging.debug('new_leaderboard:')
        logging.debug(new_leaderboard)

        all_daily_results = get_all_daily_results()
        logging.debug(all_daily_results)

        sql_date_from = '2018-11-01'
        sql_date_to = '2018-11-01'

        # logging.debug('-' * 80)
        # logging.debug('all results:')
        # results = []
        # for result in new_leaderboard:
        #     logging.debug(result)
        #     # filter by country
        #     if result['country'] in RESULTS_SUPPORTED_COUNTRIES:
        #         results.append(result)
        #
        # daily_results = []
        # if results:
        #     logging.debug('-' * 80)
        #     logging.debug('filtered results:')
        #     messages = []
        #     for num, result in enumerate(results):
        #         points = POINTS_MAP.get(num+1, 1)   # as requested, everybody gets at least 1
        #         messages.append(
        #             PUBLISH_RESULTS_LINE_TEMPLATE.format(num + 1, result['name'], result['time'], points, result['position']))
        #         daily_results.append({
        #             'position': num + 1,
        #             'name': result['name'],
        #             'points': points
        #         })
        #
        #     message = '\n\n'.join(messages)
        #     message = RECRAWL_RESULTS_HELLO_MESSAGE + '\n\n' + message + '\n\n\n' + saved_track[3]  # add URL
        #     bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
        #     logging.info("Results published")
        #
        #     if daily_results:
        #         save_daily_results_for_day(daily_results, sql_date_from, sql_date_to)
        #
        # else:
        #     logging.info("No records!")
        #     logging.debug('No records!')

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        logging.debug(error)
        import traceback
        traceback.print_exc()
        # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
        #                  text='⚠️ @antonkoba Error in publish_results: ' + str(error),
        #                  parse_mode=telegram.ParseMode.HTML)
        print(error)


if __name__ == "__main__":
    main()
