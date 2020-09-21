import random

import telegram
import requests
from bs4 import BeautifulSoup
from telegram import ParseMode

from db import update_track_of_the_day, get_track_of_the_day, get_leaderboard, save_leaderboard
from secrets import TELEGRAM_KEY, TELEGRAM_CHAT_MESSAGE_ID
from update_leaderboard import parse_leaderboard

MAP_OF_THE_DAY_MESSAGE = '🔴 Трек дня: <b>{}</b>\n' \
                         '\n' \
                         '<b>Ласкаво просимо на щоденний онлайн-турнір з дрон перегонів ім. Віктора Дзензеля!</b>\n' \
                         '\n' \
                         '🔵 Аби прийняти участь, потрібно:\n' \
                         '— запустити свою ліцензійну копію симулятору  Velocidrone (<b>v.1.16!</b>);\n' \
                         '— перевірити, що в налаштуваннях ввімкнено автопублікацію результатів;\n' \
                         '— обрати локацію та трек, відповідно до оголошеної в закріпленому повідомленні;\n' \
                         '— в налаштуваннях під час вибору траси, необхідно обрати режим Single Class - laps ' \
                         '(кількість кіл на розсуд учасника), або Single Class — 2 minutes.\n' \
                         '\n' \
                         '🔵 Обрані режими відповідають режиму Time Attack на змаганнях UADR. В залік іде кращий час кола.\n' \
                         '\n' \
                         '🔵 Рендомний трек обирається кожного дня о 17:00.\n' \
                         '🔵 Оновлення результатів кожні 5 хвилин.\n' \
                         '🔵 В кінці періоду публікується звіт з результатами щоденного турніру.\n' \
                         '\n' \
                         '🔵 Запрошуй друзів та покращуй свої результати разом із ними!\n' \
                         '\n' \
                         '🔵 Gentlemen, start your drones! Goggles down, thumbs up!\n' \
                         '\n' \
                         '🔴 Трек дня: <b>{}</b>'

CONFIG_SCENERIES = [
    (3, 'Hangar'),
    (7, 'Industrial Wasteland'),
    (8, 'Football Stadium'),
    (12, 'Countryside'),
    (13, 'Night Factory'),
    (14, 'Karting Track'),
    (15, 'Subway'),
    (16, 'Empty Scene Day'),
    (17, 'Empty Scene Night'),
    (18, 'NEC Birmingham'),
    (19, 'Warehouse'),
    (20, 'Underground Carpark'),
    (21, 'Sports Hall'),
    (22, 'Coastal'),
    (23, 'River2'),
    (24, 'City'),
    (25, 'Redbull Ring'),
    (26, 'Large Carpark'),
    (29, 'Basketball Stadium'),
    (30, 'Bando'),
    (31, 'IndoorGoKart'),
    # (32, 'Slovenia Krvavec'),  # premium
    (33, 'Dynamic Weather'),
    # (34, 'La Mothe'),  # premium
    # (35, 'Castle Sneznik'),  # premium
    # (37, 'Library'),  # premium / micros
    # (38, 'NightClub'),  # premium / micros
    # (39, 'House'),  # premium / micros
    (40, 'Future Hangar'),
    # (43, 'Future Hangar Empty'),  # not visible in Velocidrone?
]

SOUP_TRACK_LINK_CLASS = 'track-grid__li'


def get_tracks():
    # return link, scenery, track
    tracks = []
    for scenery_id, scenery_name in CONFIG_SCENERIES:
        scenery_page_url = 'https://www.velocidrone.com/leaderboard_by_version/{}/1.16'.format(scenery_id)
        response = requests.get(scenery_page_url)
        # print(response.text)
        soup = BeautifulSoup(response.content, 'html.parser')
        tracks_links = soup.findAll('div', class_=SOUP_TRACK_LINK_CLASS)
        for track_link in tracks_links:
            track_link = track_link.find('a')
            track_name = track_link.text
            track_url = track_link.get('href')
            track_info = (scenery_id, scenery_name, track_name, track_url)
            tracks.append(track_info)
            print(track_info)

    return tracks


def main():
    print("Select track script started!")

    bot = telegram.Bot(TELEGRAM_KEY)
    # print(bot)

    old_track = get_track_of_the_day()
    print('Old track: ' + str(old_track))
    previous_leaderboard = get_leaderboard()
    print('Old leaderboard: ' + str(previous_leaderboard))

    tracks = get_tracks()
    random_track = random.choice(tracks)
    print('Random track: ' + str(random_track))

    update_track_of_the_day(random_track)
    saved_track = get_track_of_the_day()
    print('Saved track: ' + str(saved_track))

    # save new leaderboard
    new_leaderboard = parse_leaderboard(saved_track)
    save_leaderboard(new_leaderboard)
    saved_leaderboard = get_leaderboard()
    print('Saved leaderboard: ' + str(saved_leaderboard))

    # post message about new track of the day
    track_text = saved_track[1] + ' - ' + saved_track[2]
    message_text = MAP_OF_THE_DAY_MESSAGE.format(track_text, track_text)
    response = bot.send_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, text=message_text, parse_mode=ParseMode.HTML)
    message_id = response.message_id
    bot.pin_chat_message(chat_id=TELEGRAM_CHAT_MESSAGE_ID, message_id=message_id)


if __name__ == "__main__":
    main()
