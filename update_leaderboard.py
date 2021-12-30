import logging

import telegram
import flag

from constants import LEADERBOARD_UPDATE_MESSAGE, LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES, USERS_BAN_LIST, \
    USERS_ALLOW_LIST
from db import get_track_of_the_day, save_leaderboard, get_leaderboard
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from utils import parse_leaderboard, compare_leaderboards

logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Leaderboard updates script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    logging.debug(bot)

    try:

        saved_track = get_track_of_the_day()
        logging.debug('-' * 80)
        logging.debug('Track of the day: ' + str(saved_track))

        previous_leaderboard = get_leaderboard()

        new_leaderboard = parse_leaderboard(saved_track)
        save_leaderboard(new_leaderboard)

        logging.debug('-' * 80)
        logging.debug('old leaderboard:')
        logging.debug(previous_leaderboard)

        logging.debug('-' * 80)
        logging.debug('new_leaderboard:')
        logging.debug(new_leaderboard)

        logging.debug('-' * 80)
        message_parts = []
        for diff in compare_leaderboards(previous_leaderboard, new_leaderboard):

            logging.debug(diff)

            # filter by country
            if diff['record']['country'] in list(LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES.keys()):

                text_position = '#' + diff['record']['position']
                improved_position = diff.get('improved_position')
                if improved_position:
                    text_position = text_position + '(#' + improved_position + ')'
                text_time = diff['record']['time'] + 's'
                improved_time = diff.get('improved_time')
                if improved_time:
                    text_time = text_time + '(-' + improved_time + 's)'
                text_name = diff['record']['name']
                version = diff['record']['version']
                if LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES.get(diff['record']['country']):
                    country_flag = flag.flag(LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES[diff['record']['country']])
                else:
                    country_flag = '🏳️'
                message_text = LEADERBOARD_UPDATE_MESSAGE.format(country_flag, text_name, text_time, text_position)

                # just to add some visibility
                if version != '1.16':
                    message_text = message_text + ' - v' + version
                # logging.debug('message_text: ' + message_text)  # might have some non-ascii chars

                if text_name.lower() not in USERS_BAN_LIST:
                    if ('*' in USERS_ALLOW_LIST) or (text_name.lower() in USERS_ALLOW_LIST):
                        message_parts.append(message_text)

            else:
                logging.debug('not supported country: ' + diff['record']['country'])

        if message_parts:
            message = '\n\n'.join(message_parts)
            bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
            logging.info("Leaderboard updated")
        else:
            logging.info("No updates!")

    except Exception as error:
        logging.exception('Uncaught error: ')
        logging.debug(error)
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in update_leaderboard: ' + str(exc),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
