import json
import logging
import telegram

from constants import PUBLISH_RESULTS_HELLO_MESSAGE, PUBLISH_RESULTS_TRACK_NAME, \
    PUBLISH_RESULTS_LINE_TEMPLATE, RESULTS_SUPPORTED_COUNTRIES, POINTS_MAP, PUBLISH_RESULTS_TAG
from db import get_track_of_the_day, save_daily_results, get_all_daily_results
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID, DB_TABLE_PREFIX
from utils import parse_leaderboard


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Total stat started!")

    # bot = telegram.Bot(TELEGRAM_KEY)
    # logging.debug(bot)

    try:
        results = get_all_daily_results()
        for res in results:
            # print(res)
            # print(json.load(res[2]))
            print(res[1] + ';' + str(len(json.load(res[2]))))

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        logging.debug(error)
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        print(exc)
        # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
        #                  text='⚠️ @antonkoba Error in publish_results: ' + str(exc),
        #                  parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
