import datetime
import random
import os

import logging
import time
import urllib

import telegram

from constants import MAP_OF_THE_DAY_MESSAGE, TRACK_POLL_TEXT, TRACK_POLL_OPTIONS, VERSION_GET_TRACKS
from db import update_track_of_the_day, get_track_of_the_day, get_leaderboard, save_leaderboard, add_track_poll
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID, PRO_MODE
from utils import parse_leaderboard, filter_tracks, get_tracks


logging.getLogger('telegram').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
log_path = os.path.dirname(os.path.realpath(__file__))
log_file = '%s/log.txt' % (log_path, )
handler = logging.FileHandler(log_file, encoding='utf8')
handler.setFormatter(formatter)
logger.addHandler(handler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(logging.StreamHandler())


def main():
    logger.info("Select track script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    # logger.debug(bot)

    try:

        # this may fail due to some non-ascii messages previously saved in the leaderboard
        # hacky fix
        try:
            old_track = get_track_of_the_day()
            logger.debug('Old track: ' + str(old_track))
            previous_leaderboard = get_leaderboard()
            logger.debug('Old leaderboard: ' + str(previous_leaderboard))
        except Exception as e:
            logging.exception('Error while printing old leaderboard:')

        # get list of all sceneries X all tracks
        tracks = get_tracks()
        tracks = filter_tracks(tracks)
        random_track = random.choice(tracks)
        logger.debug('Random track: ' + str(random_track))

        # save ToD
        update_track_of_the_day(random_track)
        saved_track = get_track_of_the_day()
        logger.debug('Saved track: ' + str(saved_track))

        # save new leaderboard
        new_leaderboard = parse_leaderboard(saved_track)
        save_leaderboard(new_leaderboard)
        saved_leaderboard = get_leaderboard()
        logger.debug('Saved leaderboard: ' + str(saved_leaderboard))

        # post message about new track of the day
        track_text = saved_track[1] + ' - ' + saved_track[2]
        date_text = datetime.datetime.now().strftime('%d.%m.%Y') + ' - ' + \
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
        search_string = urllib.parse.quote_plus(saved_track[1] + ' ' + saved_track[2])
        url_text = saved_track[3].replace(VERSION_GET_TRACKS, 'All')
        search_string = 'http://www.youtube.com/results?search_query={}&oq={}'.format(search_string, search_string)
        message_text = MAP_OF_THE_DAY_MESSAGE.format(date_text, track_text, url_text, search_string)
        response = bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message_text,
                                    parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        message_id = response.message_id
        bot.pin_chat_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, message_id=message_id)
        logger.info("Track selected")

        if not PRO_MODE:
            time.sleep(3)
            poll_message_response = bot.send_poll(
                chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                question=TRACK_POLL_TEXT.format(track_text),
                options=TRACK_POLL_OPTIONS,
                is_anonymous=True,
            )
            logger.debug('poll_message: ' + str(poll_message_response))

            # save poll message id to the DB
            add_track_poll(saved_track[0], saved_track[1], saved_track[2], saved_track[3],
                           poll_message_response.message_id, TRACK_POLL_OPTIONS)

            # test_data = {'chat': {'username': 'fpv_velocidrone_ua', 'type': 'channel', 'title': 'FPV Велосідрон 🇺🇦',
            #                       'id': -1001152818373},
            #              'photo': [], 'delete_chat_photo': False,
            #              'supergroup_chat_created': False, 'channel_chat_created': False, 'entities': [],
            #              'caption_entities': [], 'message_id': 17418,
            #              'poll': {'close_date': None, 'is_anonymous': True, 'explanation_entities': [],
            #                       'is_closed': False,
            #                       'options': [{'text': 'Кращий трек в моєму житті!', 'voter_count': 0},
            #                                   {'text': 'В фейворітс!', 'voter_count': 0},
            #                                   {'text': 'Нормальний трек', 'voter_count': 0},
            #                                   {'text': 'Так собі, можна літати', 'voter_count': 0},
            #                                   {'text': 'Не гоночний!', 'voter_count': 0},
            #                                   {'text': 'Є критичні проблеми', 'voter_count': 0}],
            #                       'total_voter_count': 0, 'allows_multiple_answers': False, 'type': 'regular',
            #                       'question': 'Як вам трек Dynamic Weather - Quad Rivals Ladders from Hell DW?\n\n#velocibotpoll',
            #                       'id': '5424730049184006219'
            #                       },
            #              'date': 1642690932, 'new_chat_members': [],
            #              'new_chat_photo': [], 'group_chat_created': False
            #              }

    except Exception as error:
        logging.exception(error)
        logger.debug('Uncaught error: ')
        import traceback
        exc = traceback.format_exc()
        logger.error(exc)
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in select_track: ' + str(exc),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
