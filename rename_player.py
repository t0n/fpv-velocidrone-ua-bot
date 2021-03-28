import logging
import telegram

from constants import PUBLISH_RESULTS_HELLO_MESSAGE, PUBLISH_RESULTS_LINE_TEMPLATE, RESULTS_SUPPORTED_COUNTRIES, \
    POINTS_MAP, RENAME_PLAYER_TEMPLATE
from db import get_track_of_the_day, save_daily_results, get_all_daily_results
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from utils import parse_leaderboard


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Rename player script started!")

    # bot = telegram.Bot(TELEGRAM_KEY)
    # print(bot)

    rename_from = 'AntonKoba'
    rename_to = 'AntonTest'
    print('Renaming player from ' + rename_from + ' to ' + rename_to)

    affected_results = 0

    try:

        all_daily_results = get_all_daily_results()
        print(all_daily_results)

        for daily_result in all_daily_results:
            # data =
            pass

        if affected_results:
            pass
            # message = RENAME_PLAYER_TEMPLATE.format()
            # # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
            # logging.info("Message published")

    except Exception as error:
        logging.exception(error)
        print('Uncaught error: ')
        print(error)
        import traceback
        traceback.print_exc()
        # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
        #                  text='⚠️ @antonkoba Error in rename_player: ' + str(error),
        #                  parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
