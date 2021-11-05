"""
Common/shared constants
"""


GAME_MODE_1_LAP = '1lap'
GAME_MODE_3_LAPS = '3laps'
GAME_MODE_URLS = {
    GAME_MODE_1_LAP: 'https://www.velocidrone.com/set_race_mode/3',  # Race Mode: Single Class
    GAME_MODE_3_LAPS: 'https://www.velocidrone.com/set_race_mode/6',  # 3 Lap: Single Class
}

ACTIVE_GAME_MODE = GAME_MODE_3_LAPS


"""
Section: Leaderboard Updates
"""


LEADERBOARD_UPDATE_MESSAGE = '{} <b>{}</b> - {} / <b>{}</b>'  # starts with flag emoji

LEADERBOARD_UPDATES_SUPPORTED_COUNTRIES = {
    'Ukraine': 'UA',
}

LEADERBOARD_DAYS_LOOKBACK = 1
LEADERBOARD_DATE_FORMAT = '%d/%m/%Y'


"""
Section: Select Track
"""


MAP_OF_THE_DAY_MESSAGE = '🏁 Трек дня: <b>{}</b>\n' \
                         '\n' \
                         '<b>Ласкаво просимо на щоденний онлайн-турнір з дрон перегонів ім. Віктора Дзензеля!</b>\n' \
                         '\n' \
                         'Умови за посиланням:' \
                         'http://sim.droner.com.ua' \
                         '\n' \
                         '\n' \
                         'Запрошуй друзів та покращуй свої результати разом із ними!\n' \
                         '\n' \
                         '#velocibottotd\n' \
                         '\n' \
                         '🏁 Трек дня: <b>{}</b>' \
                         '\n\n\n'

CONFIG_SCENERIES = [
    (3, 'Hangar'),
    (7, 'Industrial Wasteland'),
    (8, 'Football Stadium'),
    (12, 'Countryside'),
    # (13, 'Night Factory'),  # removed in new version
    # (14, 'Karting Track'),  # all tracks have bad performance
    (15, 'Subway'),
    (16, 'Empty Scene Day'),
    (17, 'Empty Scene Night'),
    (18, 'NEC Birmingham'),
    # (19, 'Warehouse'),  # removed in new version
    (20, 'Underground Carpark'),
    # (21, 'Sports Hall'),  # too small maps here / micros?
    (22, 'Coastal'),
    (23, 'River2'),
    (24, 'City'),
    # (25, 'Redbull Ring'),  # removed in new version
    (26, 'Large Carpark'),
    # (29, 'Basketball Stadium'),  # guys said there are no good tracks there
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
    'redbull dr.one',  # 'Redbull Ring - Redbull DR.ONE' - finish gates hard to hit
    'vrl season 3 track 3',  # too long, moving obstacles
    'vrl team championships',  # too long
    'growers rock garden',  # 'Dynamic Weather - Growers Rock Garden' - long/ bad navigation
    'vrl season 7 championships',  # 'Dynamic Weather - VRL Season 7 Championships' - too long?
    # 'quad rivals trainer level 3 dw',  # 'Dynamic Weather - Quad Rivals Trainer Level 3 DW' -- this should be ok
    'gokartrelay',  # slow or  something
    'gods_of_quadhalla',  # ppl didn't like it
    'vrl-freestyle-country',
    'newbeedrone',  # whoop tracks
    'boners journey',  # 246 gates
    'world of war',  # bugs
    'corona',
    'whoop',
    'neon cage',  # whoops?
]

DO_NOT_REPEAT_TRACK_FOR_DAYS = 90


"""
Section: Publish results
"""


PUBLISH_RESULTS_HELLO_MESSAGE = '🇺🇦🏁🇺🇦 Результати дня 🇺🇦🏁🇺🇦'
PUBLISH_RESULTS_TRACK_NAME = 'Трек дня: <b>{}</b>'
PUBLISH_RESULTS_TAG = '#velocibotdaily'

RECRAWL_RESULTS_HELLO_MESSAGE = 'FIXED FIXED - Результати дня - FIXED FIXED'

PUBLISH_RESULTS_LINE_TEMPLATE = '<b>#{}</b> - <b>{}</b> - {}s / <b>Балів: {}</b>\n<i>(#{} в загальному заліку треку)</i>'

RESULTS_SUPPORTED_COUNTRIES = [
    'Ukraine',
]

# new suggestion for 30 winners
# 2, 3, 5, 7, 10, 13, 16, 19, 23, 27,
# 31, 35, 39, 44, 49, 54, 60, 66, 72, 79,
# 86, 94, 102, 112, 123, 135, 150, 167, 186, 225
POINTS_MAP = {
    1: 85,
    2: 72,
    3: 66,
    4: 60,
    5: 54,
    6: 49,
    7: 44,
    8: 39,
    9: 35,
    10: 31,
    11: 27,
    12: 23,
    13: 19,
    14: 16,
    15: 13,
    16: 10,
    17: 7,
    18: 5,
    19: 3,
    20: 2,
}
# 85, 72, 66, 60, 54, 49, 44, 39, 35, 31, 27, 23, 19, 16, 13, 10, 7, 5, 3, 2,


"""
Monthly results
"""

MONTHLY_RESULTS_LINE = '<b>#{}</b> - <b>{}</b> - {} балів'
MONTHLY_RESULTS_TIME_INTERVAL = '({} - {})'
MONTHLY_DAILY_RESULTS = '🇺🇦🏁🇺🇦 Проміжні результати місяця 🇺🇦🏁🇺🇦\n{}\n\n{}\n\n#velocibotmonthly\n\n'
MONTHLY_FINAL_RESULTS = '🇺🇦🏆🥇🏆🇺🇦 Фінальні результати місяця 🇺🇦🏆🥇🏆🇺🇦\n{}\n\n{}\n\n#velocibotmonthlyfinal\n\n'


"""
Rename player
"""

RENAME_PLAYER_TEMPLATE = 'Пілот <b>{}</b> був переіменований в <b>{}</b> (офіційно)\n' \
                         '<i>Наступні результати дня/місяця можуть бути перераховані</i>'


PATRONS_TEXT = '🙇🙏 Розвиток проекту можливий завдяки донатерам: {}.\n\nВи також можете підтримати проект: https://www.patreon.com/kwadd\n\n'
PATRONS_LIST = [
    'Іван Норожнов',
    'Lef',
    'Влад',
    'Alexey Gorbach',
]


"""
More talking
"""
# TODO add bot responses for results in top-3, top-10, >190 and others (whether improved time or not)


"""
Ban list
"""
USERS_BAN_LIST = [
    '.scissors',
]
