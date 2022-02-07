"""
Common/shared constants
"""
from secrets import PRO_MODE

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


MAP_OF_THE_DAY_MESSAGE = '🏁 Трек дня {}:\n<b>{}</b>\n' \
                         '\n' \
                         '<b>Ласкаво просимо на щоденний онлайн-турнір з дрон перегонів ім. Віктора Дзензеля!</b>\n' \
                         '\n' \
                         'Умови за посиланням: ' \
                         'http://sim.droner.com.ua' \
                         '\n' \
                         '\n' \
                         'Запрошуй друзів та покращуй свої результати разом із ними!\n' \
                         '\n' \
                         '#velocibottotd\n' \
                         '\n' \
                         'Лідерборд:\n<b>{}</b>\n' \
                         '\n' \
                         'Шукати трек на YouTube:\n<b>{}</b>' \
                         '\n\n\n'
if PRO_MODE:
    MAP_OF_THE_DAY_MESSAGE = '👑 Трек дня {}:\n<b>{}</b>\n' \
                             '\n' \
                             '#velocibotPROtotd\n' \
                             '\n' \
                             'Лідерборд:\n<b>{}</b>\n' \
                             '\n' \
                             'Шукати трек на YouTube:\n<b>{}</b>' \
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
if PRO_MODE:
    CONFIG_SCENERIES = [
        (8, 'Football Stadium'),
        (16, 'Empty Scene Day'),
        (33, 'Dynamic Weather'),
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
    'tbs spec 4',  # (Bando) wires, stupid track
    'tdl races - gamex 2019',  # sometimes gates does not count
    'opg ',  # freestyle maps
    'boners bando towers',  # crazy track (
    'vrl-freestyle-coast',  # we hate freestyle
    'boners bonsai fpv 4 freestyle',
    'freestyle_tower_of_magical_power',  # just seems suspicious
    'dragons_and_wizards',  # just seems suspicious
    'trainer',
    'tropical heat',
    'boners bando',
    'rona masters',
    # TODO check these tracks - too few results/strange titles?
    # Dutchman ?
    # Rock around the rocks ?
    # Football Stadium - Inflatable Insanity ?
    # River2 - SFPV Matterhorn ?
    # Reindeer-Raceoff ?
    # River2 - SFPV Game of Drones ?
    # trollrace ?
    # Dynamic Weather - Kumos_Purgatory ?
    # Quadcopters Track ?
    # RollerCoasterRace1 ?
    # River2 - SFPV H20Fire ?
    # Dynamic Weather - Quad Rivals Who Works DW ?
    # Dynamic Weather - Palmtree fpv 4 ?
    # Dynamic Weather - QuadLantis ?
    # TOG - Rona Masters ?
    # Dynamic Weather - aquafpv 2 ?
    # Dynamic Weather - medieval fpv ?
    # Dynamic Weather - Why Nut ?
    # Proximity ?
    # Dynamic Weather - X-mas fpv 2021 ?
    # Prodangles pylon race ?
    # Dynamic Weather - Growers Rock Garden ?
    # Empty Scene Day - Quad Rivals 2021 Race 9 - Holiday Hootenanny ?
    # Empty Scene Day - TOG - Shake-It-Off ?
    # Empty Scene Day - Laxton-June-2019 ?
    # Dynamic Weather - Lord of the Rings ?
    # Dynamic Weather - Haunted forest 4  ?
    # Empty Scene Night - Skatfpv ?
    # Dynamic Weather - Boners Woody II ?
]
if PRO_MODE:
    TRACK_NAMES_BLOCK_LIST += [
        'vrl',  # ALL VRL :)
        'school is cancelled',
        'train insane',  # good for training though
        '2014',
        '2015',
        '2016',
        '2017',
        '2018',
        '2019',
        '2020',
        'level',  # all those training tracks
        'fpv dutchman mad house',  # Alexander says it's khuinya
        'full of flow',  # Alexander says it's pizdets
        'mayhem dawn till dusk',  # Alexandre says it's shit
        'firedrill',
        'bando',
    ]
else:
    # add blocked tracks for normal mode only (block too 'tight' over-flown tracks)
    TRACK_NAMES_BLOCK_LIST += []

DO_NOT_REPEAT_TRACK_FOR_DAYS = 90
if PRO_MODE:
    DO_NOT_REPEAT_TRACK_FOR_DAYS = 60

"""
Section: Publish results
"""


PUBLISH_RESULTS_HELLO_MESSAGE = '🇺🇦🏁🇺🇦 Результати дня 🇺🇦🏁🇺🇦'
if PRO_MODE:
    PUBLISH_RESULTS_HELLO_MESSAGE = '👑 Результати дня 👑'

PUBLISH_RESULTS_TRACK_NAME = 'Трек дня: <b>{}</b>'
PUBLISH_RESULTS_TAG = '#velocibotdaily'
if PRO_MODE:
    PUBLISH_RESULTS_TAG = '#velocibotPROdaily'

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
if PRO_MODE:
    MONTHLY_DAILY_RESULTS = '👑 Проміжні результати місяця 👑\n{}\n\n{}\n\n#velocibotPROmonthly\n\n'
    MONTHLY_FINAL_RESULTS = '👑 Фінальні результати місяця 👑\n{}\n\n{}\n\n#velocibotPROmonthlyfinal\n\n'


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
    'K1R',
    'Alexandr Malovanchuk',
    'Oleh Novosad',
]
if PRO_MODE:
    PATRONS_TEXT = '{}'
    PATRONS_LIST = []

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
USERS_ALLOW_LIST = ['*', ]
if PRO_MODE:
    USERS_BAN_LIST = [
        '.scissors',
    ]
    # top-12 for 2021 & top-12 for Jan 2022
    USERS_ALLOW_LIST = [
        'K1R',
        'lef',
        'YANIS FPV',
        'Dmytro Avdosiev',
        'WordyN',
        'Dronius',
        'alexfmn',
        'Slashchev',
        'Sergii Send_it',
        'g0rsky',
        'aviakpdu',
        'StDuck',
        'severteka',
        '4ndro1d78',
        'FalconFPV',
        '_ra',
        'anton. fpv',
        'SashPRO',
    ]


"""
Polls
"""
TRACK_POLL_TEXT = 'Як вам трек {}?\n\n#velocibotpoll'
TRACK_POLL_OPTIONS = [
    '[ 10] - Кращий трек в моєму житті!',
    '[  5] - В фейворітс!',
    '[  3] - Нормальний трек',
    '[  1] - Так собі, можна літати',
    '[ -1] - Не гоночний!',
    '[ -5] - Трек лайно!',
    '[-10] - Є критичні проблеми (не зараховуються ворота і тд)',
]
TRACK_POLL_RESULTS = 'Голосування за трек <b>{}</b> завершено!\n\nВсього голосів: {}\n' \
                     'Середня оцінка траси: <b>{}</b>\n\n' \
                     '#velocibotpollresults'
