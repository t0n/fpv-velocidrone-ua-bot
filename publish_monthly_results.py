import json
import logging
from datetime import datetime

import telegram

from constants import PUBLISH_RESULTS_LINE_TEMPLATE, MONTHLY_RESULTS_LINE, MONTHLY_FINAL_RESULTS, MONTHLY_DAILY_RESULTS, \
    MONTHLY_RESULTS_TIME_INTERVAL
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
    logging.debug(bot)

    try:

        day = datetime.today().day

        if 1 == day:
            # this is real monthly announcement of final results for previous month
            get_previous_month = True
        else:
            # this is testing or intermediate results
            get_previous_month = False

        all_daily_results = get_daily_results(get_previous_month)

        points_per_name = {}

        all_dates = []

        logging.debug('all_daily_results: ' + str(all_daily_results))

        for day_results in all_daily_results:
            logging.debug('day_results in all_daily_results: ' + str(day_results))

            logging.debug('-' * 80)

            results_date = day_results[1]
            logging.debug('results_date: ' + str(results_date))
            all_dates.append(results_date)

            results = json.loads(day_results[2])  # data column
            logging.debug('results: ' + str(results))

            for result in results:
                logging.debug('result: ' + str(result))
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
                # if this is 0 points - it should be 1 point
                results_of_the_day = results_of_the_day if results_of_the_day > 0 else 1

                total_points_for_name += results_of_the_day
                points_per_name[result['name']] = total_points_for_name

        logging.debug('=' * 80)
        logging.debug('points_per_name: ' + str(points_per_name))

        monthly_leaderboard = sorted(points_per_name.items(), key=lambda x: x[1], reverse=True)
        logging.debug('monthly_leaderboard: ' + str(monthly_leaderboard))

        messages = []
        for pos, monthly_leaderboard_item in enumerate(monthly_leaderboard):
            logging.debug('pos: ' + str(pos+1))
            logging.debug('monthly_leaderboard_item: ' + str(monthly_leaderboard_item))
            messages.append(MONTHLY_RESULTS_LINE.format(pos+1, monthly_leaderboard_item[0], monthly_leaderboard_item[1]))
        message = '\n\n'.join(messages)

        logging.debug('all_dates: ' + str(all_dates))
        if all_dates:

            # not real dates
            # min_date = min(all_dates).strftime('%d.%m.%Y')
            # max_date = max(all_dates).strftime('%d.%m.%Y')
            min_date = min(all_dates)[:10]
            max_date = max(all_dates)[:10]
            logging.debug('days min: ' + str(min_date))
            logging.debug('days max: ' + str(max_date))
            time_interval = MONTHLY_RESULTS_TIME_INTERVAL.format(min_date, max_date)

        else:
            logging.error("all_dates is empty")
            time_interval = '???'

        if 1 == day:
            # this is real monthly announcement of final results for previous month
            message = MONTHLY_FINAL_RESULTS.format(time_interval, message)
        else:
            # this is testing or intermediate results
            message = MONTHLY_DAILY_RESULTS.format(time_interval, message)

        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=telegram.ParseMode.HTML)
        logging.info("Results published")

    except Exception as error:
        logging.exception(error)
        logging.debug('Uncaught error: ')
        logging.debug(error)
        import traceback
        exc = traceback.format_exc()
        logging.error(exc)
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID,
                         text='⚠️ @antonkoba Error in publish_monthly_results: ' + str(exc),
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == "__main__":
    main()
