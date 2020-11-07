from _decimal import Decimal

import telegram
import requests
import flag
from bs4 import BeautifulSoup
from telegram import ParseMode

from db import get_track_of_the_day, save_leaderboard, get_leaderboard
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID


LEADERBOARD_UPDATE_MESSAGE = '{} <b>{}</b> - {} / <b>{}</b>'  # starts with flag emoji

SUPPORTED_COUNTRIES = {
    'Ukraine': 'UA',
    'Russian Federation': 'RU',  # do we need it?
    'Belarus': 'BY',

    'Poland': 'PL',
    'Hungary': 'HU',
    'Czech Republic': 'CZ',
}


# TODO change to parsing leaderboards for all versions
def parse_leaderboard(track_info):
    print('track_info: ' + str(track_info))

    track_leaderboard_url = track_info[3]
    print('track_leaderboard_url: ' + str(track_leaderboard_url))

    # TODO remove
    # if track_leaderboard_url.endswith('All'):
    #     track_leaderboard_url = track_leaderboard_url.replace('/All', '/1.16')

    response = requests.get(track_leaderboard_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    records = []
    rows = soup.find('tbody').findAll('tr')
    for row in rows:
        try:
            # print('row: ' + str(row))
            cells = row.findAll('td')
            new_record = {
                'position': cells[0].text,
                'time': cells[1].text,
                'name': bytes(cells[2].text.strip(), 'utf-8').decode('utf-8', 'ignore'),
                'country': cells[3].text.strip(),
                'ranking': cells[4].text,
                'model': cells[5].text.strip(),
                'date': cells[6].text,
                # TODO update version below VVVVVV
                'version': cells[7].text if len(cells) > 7 else '1.16',  # okay there might be no version here
            }
            print('new_record: ' + str(new_record))
            records.append(new_record)
        except Exception as e:
            print('Cannot parse row!')
            try:
                print(row.encode('utf-8'))
            except Exception:
                pass
            print(e)
            print('continuing...')
    return records


def compare_leaderboards(old, new):
    updates = []
    for new_record in new:
        old_record_found = False
        # Update: sometimes there are 2 records by same player but different versions, so we need to dedup
        for old_record in old:

            # TODO remove this later
            # if 'version' not in old_record:
            #     old_record['version'] = -1

            if old_record['name'] == new_record['name'] and old_record['version'] == new_record['version']:
                old_record_found = True
                if Decimal(new_record['time']) < Decimal(old_record['time']):
                    updates.append({
                        'record': new_record,
                        'improved_time': str(Decimal(old_record['time']) - Decimal(new_record['time'])),
                        'improved_position': old_record['position'],
                    })
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

    new_leaderboard = parse_leaderboard(saved_track)
    save_leaderboard(new_leaderboard)

    print('-' * 80)
    print('old leaderboard:')
    print(previous_leaderboard)

    print('-' * 80)
    print('new_leaderboard:')
    print(new_leaderboard)

    message_parts = []
    for diff in compare_leaderboards(previous_leaderboard, new_leaderboard):

        print(diff)

        # filter by country
        if diff['record']['country'] in list(SUPPORTED_COUNTRIES.keys()):

            text_position = '#' + diff['record']['position']
            improved_position = diff.get('improved_position')
            if improved_position:
                text_position = text_position + '(#' + improved_position + ')'
            text_time = diff['record']['time'] + 's'
            improved_time = diff.get('improved_time')
            if improved_time:
                text_time = text_time + '(-' + improved_time + 's)'
            text_name = diff['record']['name']
            country_flag = flag.flag(SUPPORTED_COUNTRIES[diff['record']['country']])
            message_text = LEADERBOARD_UPDATE_MESSAGE.format(country_flag, text_name, text_time, text_position)
            print('message_text: ' + message_text)

            message_parts.append(message_text)

        else:
            print('not supported country: ' + diff['record']['country'])

    if message_parts:
        message = '\n\n'.join(message_parts)
        print('-' * 80)
        print('message: ' + str(message))
        bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message, parse_mode=ParseMode.HTML)
    else:
        print('No updates!')


if __name__ == "__main__":
    main()
