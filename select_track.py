import random

import logging
import telegram

from constants import MAP_OF_THE_DAY_MESSAGE, TRACK_POLL_TEXT, TRACK_POLL_OPTIONS
from db import update_track_of_the_day, get_track_of_the_day, get_leaderboard, save_leaderboard
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from utils import parse_leaderboard, filter_tracks, get_tracks


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Select track script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    # logging.debug(bot)

    try:

        # this may fail due to some non-ascii messages previously saved in the leaderboard
        # hacky fix
        try:
            old_track = get_track_of_the_day()
            logging.debug('Old track: ' + str(old_track))
            previous_leaderboard = get_leaderboard()
            logging.debug('Old leaderboard: ' + str(previous_leaderboard))
        except Exception as e:
            logging.exception('Error while printing old leaderboard:')

        # get list of all sceneries X all tracks
        tracks = get_tracks()
        tracks = filter_tracks(tracks)
        random_track = random.choice(tracks)
        logging.debug('Random track: ' + str(random_track))

        # save ToD
        update_track_of_the_day(random_track)
        saved_track = get_track_of_the_day()
        logging.debug('Saved track: ' + str(saved_track))

        # save new leaderboard
        new_leaderboard = parse_leaderboard(saved_track)
        save_leaderboard(new_leaderboard)
        saved_leaderboard = get_leaderboard()
        logging.debug('Saved leaderboard: ' + str(saved_leaderboard))

        # post message about new track of the day
        track_text = saved_track[1] + ' - ' + saved_track[2]
        message_text = MAP_OF_THE_DAY_MESSAGE.format(track_text, track_text)
        response = bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message_text,
                                    parse_mode=telegram.ParseMode.HTML)
        message_id = response.message_id
        bot.pin_chat_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, message_id=message_id)
        logging.info("Track selected")

        poll_message = bot.send_poll(
            chat_id=TELEGRAM_CHAT_MESSAGE_ID,
            question=TRACK_POLL_TEXT,
            options=TRACK_POLL_OPTIONS,
            is_anonymous=False,
            open_period=24*60*60,
        )
        logging.debug(f'poll_message: {poll_message}')

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in select_track: ' + str(exc),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
