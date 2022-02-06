import random

import logging
import time

import telegram

from constants import MAP_OF_THE_DAY_MESSAGE, TRACK_POLL_TEXT, TRACK_POLL_OPTIONS
from db import update_track_of_the_day, get_track_of_the_day, get_leaderboard, save_leaderboard, get_latest_track_poll
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID, PRO_MODE
from utils import parse_leaderboard, filter_tracks, get_tracks


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Select track script started!")

    bot = telegram.Bot(TELEGRAM_KEY)

    try:

        latest_poll_data = get_latest_track_poll()
        logging.info(latest_poll_data)

        """
        'id integer PRIMARY KEY,' \
        'date datetime DEFAULT CURRENT_TIMESTAMP, ' \
        'scenery_id integer NOT NULL, ' \
        'scenery_name text NOT NULL, ' \
        'track_name text NOT NULL, ' \
        'track_url  text NOT NULL,' \
        'poll_message_id  text NOT NULL,' \
        'options  text NOT NULL,' \
        """

        message_id = latest_poll_data[6]
        poll_options = latest_poll_data[7]

        # send STOP command
        stop_response = bot.stop_poll(
            chat_id=TELEGRAM_CHAT_MESSAGE_ID,
            message_id=message_id
        )
        logging.info('stop_response: ' + str(stop_response))
        """
        stop_response: {'id': '5431897744010641587', 'question': 'Test Poll', 'options': [{'text': 'option1', 
        'voter_count': 1}, {'text': 'option2', 'voter_count': 0}], 'total_voter_count': 1, 'is_closed': True, 
        'is_anonymous': True, 'type': 'regular', 'allows_multiple_answers': False, 'explanation_entities': [], 
        'close_date': None}
        """

        answers = stop_response.options  # text, voters_count
        total_points = 0
        total_voters = 0
        for option in poll_options:
            logging.debug('looking for option: ' + str(option))
            found_in_answers = None
            for answer in answers:
                if answer.text == option:
                    found_in_answers = answer
            if found_in_answers:
                logging.debug('found option in answers: ' + str(found_in_answers))
                try:
                    # TODO parse points e.g. `[ 10] - Кращий трек в моєму житті!`
                    parsed_points = int(found_in_answers.text[1, 4])
                    logging.debug('parsed_points: ' + str(parsed_points))
                    points = parsed_points * found_in_answers.voter_count
                    logging.debug('points: ' + str(points))
                    total_voters += found_in_answers.voter_count
                    total_points += points
                except Exception as e:
                    logging.error('Cannot parse ' + str(found_in_answers))
        if total_voters:
            average_points = float(total_points) / float(total_voters)  # TODO round up
        else:
            average_points = 0
        logging.debug('average_points: ' + str(average_points))

        # TODO save to DB

        # TODO write a message
    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in stop_selected_track_poll: ' + str(exc),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
