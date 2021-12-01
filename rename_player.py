import json
import logging
import telegram

from constants import RENAME_PLAYER_TEMPLATE
from db import get_all_daily_results, update_daily_results
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Rename player script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    logging.debug(bot)

    rename_from = 'sergii23'
    rename_to = 'Sergii Send_it'
    logging.debug('Renaming player from ' + rename_from + ' to ' + rename_to)

    affected_results = 0

    try:

        all_daily_results = get_all_daily_results()
        logging.debug(all_daily_results)

        for daily_result in all_daily_results:
            res_id = daily_result[0]
            res_data = daily_result[2]
            logging.debug('=' * 80)
            logging.debug(res_id)
            logging.debug('=' * 80)
            data = json.loads(res_data)
            found_changes = False
            for single_res in data:
                logging.debug(single_res)
                if single_res['name'] == rename_from:
                    single_res['name'] = rename_to
                    found_changes = True
                    logging.debug('making replacement')
            if found_changes:
                affected_results += 1
                data_to_write = json.dumps(data)
                logging.debug('data_to_write: ' + str(data_to_write))
                update_daily_results(res_id, data_to_write)

        if affected_results:
            logging.debug('total affected results: ' + str(affected_results))
            message = RENAME_PLAYER_TEMPLATE.format(rename_from, rename_to)
            bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
            logging.info("Message published")

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        logging.debug(error)
        import traceback
        traceback.print_exc()
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in rename_player: ' + str(error),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
