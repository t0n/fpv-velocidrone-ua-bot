# import random

import logging
import time

# import telegram

# from constants import MAP_OF_THE_DAY_MESSAGE, TRACK_POLL_TEXT, TRACK_POLL_OPTIONS
from db import get_all_track_results, clear_all_track_results, add_all_track_result
# from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from utils import parse_leaderboard, filter_tracks, get_tracks, parse_full_leaderboard

logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Select track script started!")

    # bot = telegram.Bot(TELEGRAM_KEY)
    # logging.debug(bot)

    track_records = []

    try:

        # get list of all sceneries X all tracks
        tracks = get_tracks()

        # get number of tracks per location
        # # group by locations
        # list_to_group = [
        #     'Football Stadium',
        #     'Empty Scene Day',
        #     'Dynamic Weather',
        # ]
        # group_results = {}
        #
        # for track in tracks:
        #     if track[1] in list_to_group:
        #         list_per_location = group_results.get(track[1], [])
        #         list_per_location.append((track[1], track[2]))
        #         group_results[track[1]] = list_per_location
        #
        # print(group_results)
        #
        # for k, v in group_results.items():
        #     print(k)
        #     print(len(v))
        #
        # return

        # get locations with 'freestyle' in it
        for track in tracks:
            if 'freestyle' in track[2].lower():
                print(track[1] + ' - ' + track[2])

        counter = 0

        for track in tracks:
            print('parsing track ' + str(counter) + ' of ' + str(len(tracks)))
            time.sleep(2)

            logging.debug('parsing track: ' + str(track))

            # save new leaderboard
            leaderboard = parse_full_leaderboard(track)
            logging.debug('leaderboard: ' + str(leaderboard))

            track_records.append({
                'track': track,
                'leaderboard': leaderboard
            })
            counter += 1

        if track_records:
            clear_all_track_results()
            for track_record in track_records:
                track = track_record['track']
                leaderboard = track_record['leaderboard']
                for leaderboard_record in leaderboard:
                    add_all_track_result(
                        scenery_id=track[0],
                        scenery_name=track[1],
                        track_name=track[2],
                        track_url=track[3],
                        position=leaderboard_record['position'],
                        time=leaderboard_record['time'],
                        name=leaderboard_record['name'],
                        country=leaderboard_record['country'],
                        ranking=leaderboard_record['ranking'],
                        model=leaderboard_record['model'],
                        date=leaderboard_record['date'],
                        version=leaderboard_record['version']
                    )

        saved_track_results = get_all_track_results()
        print('saved_track_results: ' + str(saved_track_results))

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
        #                  text='⚠️ @antonkoba Error in select_track: ' + str(exc),
        #                  parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
