"""
Common/shared functions
"""

from _decimal import Decimal

import requests
from bs4 import BeautifulSoup

from constants import TRACK_NAMES_BLOCK_LIST, CONFIG_SCENERIES, VERSION_GET_TRACKS, SOUP_TRACK_LINK_CLASS, \
    VERSIONS_GET_LEADERBOARDS


def parse_leaderboard(track_info):
    print('track_info: ' + str(track_info))

    # original track is saved with a default version (1.16) - see
    track_leaderboard_url = track_info[3]
    print('track_leaderboard_url: ' + str(track_leaderboard_url))

    all_results = []
    for version in VERSIONS_GET_LEADERBOARDS:
        version_specific_url = track_leaderboard_url.replace(VERSION_GET_TRACKS, version)
        all_results.extend(parse_leaderboard_by_url(version_specific_url, version))
    return all_results


def parse_leaderboard_by_url(track_leaderboard_url, version):

    response = requests.get(track_leaderboard_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    records = []
    rows = soup.find('tbody').findAll('tr')
    for row in rows:
        new_record = None
        try:
            # print('row: ' + str(row))
            cells = row.findAll('td')
            new_record = {
                'position': cells[0].text,
                'time': cells[1].text,
                'name': bytes(cells[2].text.strip(), 'utf-8').decode('utf-8', 'ignore'),  # TODO: is this working?
                'country': cells[3].text.strip(),
                'ranking': cells[4].text,
                'model': cells[5].text.strip(),
                'date': cells[6].text,
                'version': cells[7].text if len(cells) > 7 else version,
            }
            print('new_record: ' + str(new_record))
            records.append(new_record)
        except Exception as e:
            print('Cannot parse row!')
            print('e')
            try:
                print(row.encode('utf-8'))
            except Exception:
                pass
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


def filter_tracks(tracks_in):
    tracks_out = []
    for scenery_id, scenery_name, track_name, track_url in tracks_in:
        excluded = False
        for block_name in TRACK_NAMES_BLOCK_LIST:
            if block_name in track_name.lower():
                excluded = True
                print('TRACK EXCLUDED: ' + str((scenery_id, scenery_name, track_name, track_url)))
        if not excluded:
            tracks_out.append((scenery_id, scenery_name, track_name, track_url))
    return tracks_out


def get_tracks():
    # return link, scenery, track
    tracks = []
    for scenery_id, scenery_name in CONFIG_SCENERIES:
        scenery_page_url = 'https://www.velocidrone.com/leaderboard_by_version/{}/{}'.format(scenery_id,
                                                                                             VERSION_GET_TRACKS)
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