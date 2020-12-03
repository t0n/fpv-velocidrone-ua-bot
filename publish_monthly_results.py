import json
import logging
from datetime import datetime

import telegram

from constants import PUBLISH_RESULTS_LINE_TEMPLATE, MONTHLY_RESULTS_LINE, MONTHLY_FINAL_RESULTS, MONTHLY_DAILY_RESULTS
from db import get_daily_results
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID


logging.basicConfig(filename='log.txt', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    # datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.ERROR)


def main():
    logging.info("Publish MONTHLY results script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    print(bot)

    try:

        day = datetime.today().day

        if 1 == day:
            # this is real monthly announcement of final results for previous month
            get_previous_month = True
        else:
            # this is testing or intermediate results
            get_previous_month = False

        get_previous_month = True  # TODO remove this is a debug
        all_daily_results = get_daily_results(get_previous_month)

        points_per_name = {}

        for day_results in all_daily_results:
            results = json.loads(day_results[2])  # data column
            print('-' * 80)
            print('results: ' + str(results))

            for result in results:
                print('result: ' + str(result))

                """
                {
                    'position': ...,
                    'name': ...
                    'points': ...
                }
                """

                total_points_for_name = points_per_name.get(result['name'], 0)
                results_of_the_day = result['points']

                # TODO remove later
                # fix for those who get 0 points at the beginning
                results_of_the_day = results_of_the_day if results_of_the_day > 0 else 1

                total_points_for_name += results_of_the_day
                points_per_name[result['name']] = total_points_for_name

        print('=' * 80)
        print('points_per_name: ' + str(points_per_name))

        monthly_leaderboard = sorted(points_per_name.items(), key=lambda x: x[1], reverse=True)
        print('monthly_leaderboard: ' + str(monthly_leaderboard))

        messages = []
        for pos, monthly_leaderboard_item in enumerate(monthly_leaderboard):
            print('pos: ' + str(pos+1))
            print('monthly_leaderboard_item: ' + str(monthly_leaderboard_item))
            messages.append(MONTHLY_RESULTS_LINE.format(pos+1, monthly_leaderboard_item[0], monthly_leaderboard_item[1]))
        message = '\n\n'.join(messages)

        if 1 == day:
            # this is real monthly announcement of final results for previous month
            message = MONTHLY_FINAL_RESULTS.format(message)
        else:
            # this is testing or intermediate results
            message = MONTHLY_DAILY_RESULTS.format(message)

        # TODO uncomment this is a debug
        # bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
        # logging.info("Results published")

    except Exception as error:
        logging.exception(error)
        print('Uncaught error: ')
        print(error)
        import traceback
        traceback.print_exc()
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in publish_monthly_results: ' + str(error),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
