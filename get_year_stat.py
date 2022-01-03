import json
import logging
# import telegram

from constants import PUBLISH_RESULTS_HELLO_MESSAGE, PUBLISH_RESULTS_TRACK_NAME, \
    PUBLISH_RESULTS_LINE_TEMPLATE, RESULTS_SUPPORTED_COUNTRIES, POINTS_MAP, PUBLISH_RESULTS_TAG
from db import get_track_of_the_day, save_daily_results, get_all_daily_results, get_year_daily_results, \
    get_year_monthly_results
# from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID, DB_TABLE_PREFIX
from utils import parse_leaderboard


# logging.basicConfig(filename='log.txt', filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     # datefmt='%H:%M:%S',
#                     level=logging.DEBUG)
# logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    # logging.info("Year stat started!")

    # bot = telegram.Bot(TELEGRAM_KEY)
    # logging.debug(bot)

    try:

        results = get_year_daily_results(2021)

        # 1. #1 count - not available (not saved)
        # 2. total points
        # 3. total count of days participated + points per day average
        # 4. average position on track - not available (not saved)
        # 5. average position in daily
        # 6. average position in monthly

        total_points = dict()
        total_positions = dict()
        total_rounds = dict()
        all_dates = list()

        blocklist = ['Gay_Racergang_fpv', '.scissors', 'the23', ]

        for res in results:
            print(res)
            data = json.loads(res[2])
            for data_item in data:
                all_dates.append(res[1])

                name = data_item['name']
                if name not in blocklist:
                    position = data_item['position']
                    points = data_item['points']

                    total_points__by_name = total_points.get(name, 0)
                    total_points__by_name += points
                    total_points[name] = total_points__by_name

                    total_positions__by_name = total_positions.get(name, [])
                    total_positions__by_name.append(position)
                    total_positions[name] = total_positions__by_name

                    total_rounds__by_name = total_rounds.get(name, 0)
                    total_rounds__by_name += 1
                    total_rounds[name] = total_rounds__by_name

            # print(res[1] + ';' + str(len(json.loads(res[2]))))

        total_points = dict(sorted(total_points.items(), key=lambda item: item[1], reverse=True))
        total_positions = {n: (sum(x) / len(x)) for (n, x) in total_positions.items()}
        total_positions = dict(sorted(total_positions.items(), key=lambda item: item[1]))
        total_rounds = dict(sorted(total_rounds.items(), key=lambda item: item[1], reverse=True))

        points_per_round = dict()
        for tpk, tpv in total_points.items():
            rounds = total_rounds.get(tpk)
            if rounds:
                points_per_round[tpk] = tpv / rounds
        points_per_round = dict(sorted(points_per_round.items(), key=lambda item: item[1], reverse=True))

        print('Year 2021 [' + str(min(all_dates)) + ' - ' + str(max(all_dates)) + ']')
        print('-' * 80)
        print('Total points')
        # for n, kv in enumerate(total_points.items()):
        for n, kv in enumerate(sorted(total_points.items(), key=lambda item: item[1], reverse=True)):
            print(str(n+1) + '. ' + kv[0] + ': ' + str(kv[1]))
        print('-' * 80)
        print('Total rounds')
        for n, kv in enumerate(sorted(total_rounds.items(), key=lambda item: item[1], reverse=True)):
            print(str(n+1) + '. ' + kv[0] + ': ' + str(kv[1]))
        print('-' * 80)
        print('Average position')
        for n, kv in enumerate(sorted(total_positions.items(), key=lambda item: item[1])):
            print(str(n+1) + '. ' + kv[0] + ': ' + str(kv[1])[:5])
        print('-' * 80)
        print('Average position / round')
        for n, kv in enumerate(sorted(points_per_round.items(), key=lambda item: item[1], reverse=True)):
            print(str(n+1) + '. ' + kv[0] + ': ' + str(kv[1])[:5])

    except Exception as error:
        # logging.exception(error)
        # logging.debug('Uncaught error: ')
        # logging.debug(error)
        import traceback
        exc = traceback.format_exc()
        # logging.error(exc)
        print(exc)
        # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
        #                  text='⚠️ @antonkoba Error in publish_results: ' + str(exc),
        #                  parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
