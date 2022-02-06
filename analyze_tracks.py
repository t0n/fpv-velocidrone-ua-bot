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

    try:

        saved_track_results = get_all_track_results()
        print(len(saved_track_results))
        print(saved_track_results[0])

        tracks_info = {}
        results_per_track = {}

        track_names = [(x[2], x[3]) for x in saved_track_results]
        print(len(track_names))
        track_names = set(track_names)
        print(len(track_names))
        print('track_names:')
        print(track_names)

        for result_per_track in saved_track_results:
            scenery_name = result_per_track[2]
            track_name = result_per_track[3]
            tmp_result_per_track = results_per_track.get((scenery_name, track_name), [])
            tmp_result_per_track.append(result_per_track)
            results_per_track[(scenery_name, track_name)] = tmp_result_per_track
        # print('results_per_track:')
        # print(results_per_track)

        for scenery_name, track_name in track_names:
            all_results_of_track = results_per_track[(scenery_name, track_name)]
            # print('scenery_name:')
            # print(scenery_name)
            # print('track_name:')
            # print(track_name)
            # print('all_results_of_track:')
            # print(all_results_of_track)

            sorted_results_of_track = sorted(all_results_of_track, key=lambda item: item[1])
            # print('sorted_results_of_track:')
            # print(sorted_results_of_track)

            total_results = len(all_results_of_track)
            min_result = float(sorted_results_of_track[0][6]) if total_results > 100 else None
            max_result = float(sorted_results_of_track[-1][6]) if total_results > 100 else None
            max_result_2 = float(sorted_results_of_track[-2][6]) if total_results > 100 else None
            max_result_3 = float(sorted_results_of_track[-3][6]) if total_results > 100 else None
            low_end_deltas = [(max_result_2 - max_result_3), (max_result - max_result_2)] if total_results > 100 else None
            low_end_delta = sum(low_end_deltas) / 2 if total_results > 100 else None
            high_end_delta = max_result - min_result if total_results > 100 else None
            deltas_ratio = low_end_delta / high_end_delta if total_results > 100 else None

            tracks_info[(scenery_name, track_name)] = {
                'total_results': total_results,
                'min_result': min_result,
                'avg_low_end_delta': low_end_delta,
                'high_end_delta': high_end_delta,
                'deltas_ratio': deltas_ratio,
            }

        # print('tracks_info:')
        # print(tracks_info)

        # PART 1. Small totals - tracks that have few results, maybe something's wrong with them

        tracks_info_small_totals = {x: y for x, y in tracks_info.items() if y['total_results'] < 199}
        tracks_info_small_totals = sorted(tracks_info_small_totals.items(), key=lambda item: item[1]['total_results'])
        print('tracks_info_small_totals:')
        for k in tracks_info_small_totals:
            print('{} - {} --> total results: {}'.format(k[0][0], k[0][1], k[1]['total_results']))
        # print(tracks_info_small_totals)

        tracks_info = {x: y for x, y in tracks_info.items() if y['min_result'] is not None}

        tracks_sorted_total_results = sorted(tracks_info.items(), key=lambda item: item[1]['min_result'])
        print('tracks_sorted_total_results:')
        # print(tracks_sorted_total_results[:20])

        tracks_sorted_min_result = sorted(tracks_info, key=lambda item: item[1])
        print('tracks_sorted_min_result:')
        # print(tracks_sorted_min_result[:10])

        tracks_sorted_min_result_rev = sorted(tracks_info, key=lambda item: item[1], reverse=True)
        print('tracks_sorted_min_result_rev:')
        # print(tracks_sorted_min_result_rev[:10])

        # TODO PART 2. Too low 1st place results - too simple/training tracks? (remove for PRO)

        # TODO PART 3. Too high 1st place results - too long tracks, not interesting (remove for both)

        # TODO PART 4. Time delta for last places - too hard to get into top-200 (remove for hobby)

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        print('error')
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        print(exc)
        # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
        #                  text='⚠️ @antonkoba Error in select_track: ' + str(exc),
        #                  parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
