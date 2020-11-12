import logging

import telegram
import flag

from constants import LEADERBOARD_UPDATE_MESSAGE, LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES
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
    print(bot)

    try:

        saved_track = get_track_of_the_day()
        print('-' * 80)
        print('Track of the day: ' + str(saved_track))

        previous_leaderboard = get_leaderboard()

        new_leaderboard = parse_leaderboard(saved_track)
        save_leaderboard(new_leaderboard)

        print('-' * 80)
        print('old leaderboard:')
        print(previous_leaderboard)

        print('-' * 80)
        print('new_leaderboard:')
        print(new_leaderboard)

        print('-' * 80)
        message_parts = []
        for diff in compare_leaderboards(previous_leaderboard, new_leaderboard):

            print(diff)

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
                country_flag = flag.flag(LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES[diff['record']['country']])
                message_text = LEADERBOARD_UPDATE_MESSAGE.format(country_flag, text_name, text_time, text_position)

                # just to add some visibility
                if version != '1.16':
                    message_text = message_text + ' - v' + version
                # print('message_text: ' + message_text)  # might have some non-ascii chars

                message_parts.append(message_text)

            else:
                print('not supported country: ' + diff['record']['country'])

        if message_parts:
            message = '\n\n'.join(message_parts)
            bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
            logging.info("Leaderboard updated")
        else:
            logging.info("No updates!")
            print('No updates!')

    except Exception as error:
        logging.exception(error)
        print('Uncaught error: ')
        print(error)
        import traceback
        traceback.print_exc()
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in update_leaderboard: ' + str(error),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
