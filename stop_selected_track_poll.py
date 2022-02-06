import random

import logging
import time

import telegram

from constants import MAP_OF_THE_DAY_MESSAGE, TRACK_POLL_TEXT, TRACK_POLL_OPTIONS
from db import update_track_of_the_day, get_track_of_the_day, get_leaderboard, save_leaderboard
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID, PRO_MODE
from utils import parse_leaderboard, filter_tracks, get_tracks


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Select track script started!")

    bot = telegram.Bot('')
    # logging.debug(bot)

    poll_message_response = bot.send_poll(
        chat_id='',
        question='Test Poll',
        options=['option1', 'option2'],
        is_anonymous=True,
    )
    logging.debug('poll_message: ' + str(poll_message_response))
    print('poll_message: ' + str(poll_message_response))

    message_id = poll_message_response.message_id
    print('message_id: ' + str(message_id))

    time.sleep(10)

    stop_response = bot.stop_poll(
        chat_id='',
        message_id=message_id
    )
    print('stop_response: ' + str(stop_response))

    """
    stop_response: {'id': '5431897744010641587', 'question': 'Test Poll', 'options': [{'text': 'option1', 'voter_count': 1}, {'text': 'option2', 'voter_count': 0}], 'total_voter_count': 1, 'is_closed': True, 'is_anonymous': True, 'type': 'regular', 'allows_multiple_answers': False, 'explanation_entities': [], 'close_date': None}
    """

    answers = stop_response.options  # text, voters_count
    # TODO process answers, post results


if __name__ == "__main__":
    main()

