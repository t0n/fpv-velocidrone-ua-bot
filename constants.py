"""
Common/shared constants
"""


"""
Section: Leaderboard Updates
"""


LEADERBOARD_UPDATE_MESSAGE = '{} <b>{}</b> - {} / <b>{}</b>'  # starts with flag emoji

LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES = {
    'Ukraine': 'UA',
    'Russian Federation': 'RU',  # do we need it?
    'Belarus': 'BY',

    'Poland': 'PL',
    'Hungary': 'HU',
    'Czech Republic': 'CZ',
}

LEADERBOARD_DAYS_LOOKBACK = 1
LEADERBOARD_DATE_FORMAT = '%d/%m/%Y'


"""
Section: Select Track
"""


# MAP_OF_THE_DAY_MESSAGE = '🔴 Трек дня: <b>{}</b>\n' \
#                          '\n' \
#                          '<b>Ласкаво просимо на щоденний онлайн-турнір з дрон перегонів ім. Віктора Дзензеля!</b>\n' \
#                          '\n' \
#                          '🔵 Аби прийняти участь, потрібно:\n' \
#                          '— запустити свою ліцензійну копію симулятору Velocidrone;\n' \
#                          '— перевірити, що в налаштуваннях ввімкнено автопублікацію результатів (Options -> Main Settings -> Auto Leaderbord Time Update: Yes);\n' \
#                          '— обрати локацію та трек, відповідно до оголошеної в закріпленому повідомленні;\n' \
#                          '— в налаштуваннях під час вибору траси, необхідно обрати режим Single Class - laps ' \
#                          '(кількість кіл на розсуд учасника), або Single Class — 2 minutes.\n' \
#                          '\n' \
#                          '🔵 Обрані режими відповідають режиму Time Attack на змаганнях UADR. В залік іде кращий час кола.\n' \
#                          '\n' \
#                          '🔵 Рендомний трек обирається кожного дня о 17:00.\n' \
#                          '🔵 Оновлення результатів кожні 5 хвилин.\n' \
#                          '🔵 В кінці періоду публікується звіт з результатами щоденного турніру.\n' \
#                          '🏁 За підсумками грудня переможець отримає раму TBS Source One V3, срібний та бронзовий ' \
#                          'призери – по 5 пачок будь-яких 5” пропелерів на вибір від Drono.store\n' \
#                          '\n' \
#                          '🔵 Запрошуй друзів та покращуй свої результати разом із ними!\n' \
#                          '\n' \
#                          '🔵 Gentlemen, start your drones! Goggles down, thumbs up!\n' \
#                          '\n' \
#                          '🔴 Трек дня: <b>{}</b>'

MAP_OF_THE_DAY_MESSAGE = '🔴 Трек дня: <b>{}</b>\n' \
                         '\n' \
                         '<b>Ласкаво просимо на щоденний онлайн-турнір з дрон перегонів ім. Віктора Дзензеля!</b>\n' \
                         '\n' \
                         '<b>Кращі пілоти грудня отримають призи від Drono.store!</b>' \
                         '\n' \
                         '\n' \
                         'Умови за посиланням:' \
                         '\n' \
                         'https://drono.store/content/8-dzendzel-cup' \
                         '\n' \
                         '\n' \
                         '🔵 Запрошуй друзів та покращуй свої результати разом із ними!\n' \
                         '\n' \
                         '🔵 Gentlemen, start your drones! Goggles down, thumbs up!\n' \
                         '\n' \
                         '🔴 Трек дня: <b>{}</b>' \
                         '\n\n\n'

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
    # (21, 'Sports Hall'),  # too small maps here / micros?
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
    # (40, 'Future Hangar'),  # seems to be not loading / unable to fly tracks here
    # (43, 'Future Hangar Empty'),  # not visible in Velocidrone?
]

SOUP_TRACK_LINK_CLASS = 'track-grid__li'

VERSION_GET_TRACKS = '1.16'  # leaderboard URL wil be stored with this version in it

VERSIONS_GET_LEADERBOARDS = ['1.15', '1.16', '1.17']
# VERSIONS_GET_LEADERBOARDS = ['1.16', ]

TRACK_NAMES_BLOCK_LIST = [
    'beta',  # 'IndoorGoKart - Beta 2S Power Race 8' - whoops
    'covid',  # whoops
    'micro',  # whoops
    'pylons',  # too easy
    'collision',  # 'Countryside - Collision' - boring
]

DO_NOT_REPEAT_TRACK_FOR_DAYS = 30


"""
Section: Publish results
"""


PUBLISH_RESULTS_HELLO_MESSAGE = '🇺🇦🏁🇺🇦 Результати дня 🇺🇦🏁🇺🇦'

PUBLISH_RESULTS_LINE_TEMPLATE = '<b>#{}</b> - <b>{}</b> - {}s / <b>Балів: {}</b>\n<i>(#{} в загальному заліку треку)</i>'

RESULTS_SUPPORTED_COUNTRIES = [
    'Ukraine',
]

POINTS_MAP = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}


"""
Monthly results
"""

MONTHLY_RESULTS_LINE = '<b>#{}</b> - <b>{}</b> - {} балів'
MONTHLY_RESULTS_TIME_INTERVAL = '({} - {})'
MONTHLY_DAILY_RESULTS = '🇺🇦🏁🇺🇦 Проміжні результати місяця 🇺🇦🏁🇺🇦\n{}\n\n{}\n\n'
MONTHLY_FINAL_RESULTS = '🇺🇦🏆🥇🏆🇺🇦 Фінальні результати місяця 🇺🇦🏆🥇🏆🇺🇦\n{}\n\n{}\n\n'
