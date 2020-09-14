from _decimal import Decimal

import telegram
import requests
from bs4 import BeautifulSoup
from telegram import ParseMode

from db import get_track_of_the_day, save_leaderboard, get_leaderboard
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID


LEADERBOARD_UPDATE_MESSAGE = '🏁 <b>{}</b> ({}) - {} / <b>{}</b>'  # starts with flag emoji

SUPPORTED_COUNTRIES = [
    'Ukraine',
    'Russian Federation',  # do we need it?
    'Belarus',
]


def parse_leaderboard(track_info):
    print('track_info: ' + str(track_info))

    track_leaderboard_url = track_info[3]
    print('track_leaderboard_url: ' + str(track_leaderboard_url))

    response = requests.get(track_leaderboard_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    records = []
    rows = soup.find('tbody').findAll('tr')
    for row in rows:
        # print('row: ' + str(row))
        cells = row.findAll('td')
        new_record = {
            'position': cells[0].text,
            'time': cells[1].text,
            'name': cells[2].text.strip(),
            'country': cells[3].text.strip(),
            # 'ranking': cells[4].text,
            # 'model': cells[5].text.strip(),
            # 'date': cells[6].text,
        }
        print('new_record: ' + str(new_record))
        records.append(new_record)
    return records


def compare_leaderboards(old, new):
    updates = []
    for new_record in new:
        old_record_found = False
        for old_record in old:
            if old_record['name'] == new_record['name']:
                old_record_found = True
                if Decimal(new_record['time']) < Decimal(old_record['time']):
                    print('+++ match: new {} old {}'.format(Decimal(new_record['time']), Decimal(old_record['time'])))
                    updates.append({
                        'record': new_record,
                        'improved_time': str(Decimal(old_record['time']) - Decimal(new_record['time'])),
                        'improved_position': old_record['position'],
                    })
                else:
                    print('--- same: new {} old {}'.format(Decimal(new_record['time']), Decimal(old_record['time'])))
        if not old_record_found:
            updates.append({
                'record': new_record,
            })

    return updates


def main():
    print("Leaderboard updates script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    print(bot)

    saved_track = get_track_of_the_day()
    print('-' * 80)
    print('Track of the day: ' + str(saved_track))

    previous_leaderboard = get_leaderboard()

    print('-' * 80)
    print('old leaderboard:')
    print(previous_leaderboard)

    new_leaderboard = parse_leaderboard(saved_track)
    save_leaderboard(new_leaderboard)

    print('-' * 80)
    print('new_leaderboard:')
    print(new_leaderboard)

    print('-' * 80)
    print('old leaderboard:')
    print(previous_leaderboard)

    message_parts = []
    for diff in compare_leaderboards(previous_leaderboard, new_leaderboard):

        print(diff)

        # filter by country
        if diff['record']['country'] in SUPPORTED_COUNTRIES:

            text_position = '#' + diff['record']['position']
            improved_position = diff.get('improved_position')
            if improved_position:
                text_position = text_position + '(#' + improved_position + ')'
            text_time = diff['record']['time'] + 's'
            improved_time = diff.get('improved_time')
            if improved_time:
                text_time = text_time + '(-' + improved_time + 's)'
            text_name = diff['record']['name']
            text_country = diff['record']['country']
            message_text = LEADERBOARD_UPDATE_MESSAGE.format(text_name, text_country, text_time, text_position)
            print('message_text: ' + message_text)

            message_parts.append(message_text)

        else:
            print('not supported country: ' + diff['record']['country'])

    if message_parts:
        message = '\n\n'.join(message_parts)
        print('-' * 80)
        print('message: ' + str(message))
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    main()
