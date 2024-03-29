import json
import sqlite3

from secrets import DB_TABLE_PREFIX  # to support test instance

DB_FILE = 'main.db'


def _create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


# --------------------------------------------
# CREATE ALL DBS
# --------------------------------------------


def _create_totd_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'track_of_the_day (' \
            'id integer PRIMARY KEY,' \
            'scenery_id integer NOT NULL, ' \
            'scenery_name integer NOT NULL, ' \
            'track_name text NOT NULL, ' \
            'track_url  text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


def _create_leaderboard_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'leaderboard (' \
            'id integer PRIMARY KEY,' \
            'data text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


def _create_history_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'tracks_history (' \
            'id integer PRIMARY KEY,' \
            'date datetime DEFAULT CURRENT_TIMESTAMP, ' \
            'scenery_name integer NOT NULL, ' \
            'track_name text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


def _create_daily_results_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'daily_results (' \
            'id integer PRIMARY KEY,' \
            'date datetime DEFAULT CURRENT_TIMESTAMP, ' \
            'data text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


def _create_monthly_results_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'monthly_results (' \
            'id integer PRIMARY KEY,' \
            'date datetime DEFAULT CURRENT_TIMESTAMP, ' \
            'data text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


# for statistics
def _create_all_tracks_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'all_tracks (' \
            'id integer PRIMARY KEY,' \
            'scenery_id integer NOT NULL, ' \
            'scenery_name text NOT NULL, ' \
            'track_name text NOT NULL, ' \
            'track_url  text NOT NULL,' \
            'position  integer NOT NULL,' \
            'time  text NOT NULL,' \
            'name  text NOT NULL,' \
            'country  text NOT NULL,' \
            'ranking  text NOT NULL,' \
            'model  text NOT NULL,' \
            'date  text NOT NULL,' \
            'version  text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


def _create_track_feedback_poll_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'track_feedback_poll (' \
            'id integer PRIMARY KEY,' \
            'date datetime DEFAULT CURRENT_TIMESTAMP, ' \
            'scenery_id integer NOT NULL, ' \
            'scenery_name text NOT NULL, ' \
            'track_name text NOT NULL, ' \
            'track_url  text NOT NULL,' \
            'poll_message_id  text NOT NULL,' \
            'options  text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


def _create_track_feedback_history_table_if_not_exists(connection):
    query = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE_PREFIX + 'track_feedback_history (' \
            'id integer PRIMARY KEY,' \
            'date datetime DEFAULT CURRENT_TIMESTAMP, ' \
            'scenery_id integer NOT NULL, ' \
            'scenery_name text NOT NULL, ' \
            'track_name text NOT NULL, ' \
            'track_url  text NOT NULL,' \
            'poll_message_id  text NOT NULL,' \
            'rating  text NOT NULL,' \
            'results  text NOT NULL' \
            ');'
    try:
        c = connection.cursor()
        c.execute(query)
    except sqlite3.Error as e:
        print(e)


# --------------------------------------------
# CRUD OPERATIONS
# --------------------------------------------


# --------------------------------------------
# Select track of the day
# --------------------------------------------


def update_track_of_the_day(track_info):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_totd_table_if_not_exists(connection)
        cur = connection.cursor()
        cur.execute('DELETE FROM ' + DB_TABLE_PREFIX + 'track_of_the_day')
        connection.commit()
        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + 'track_of_the_day(scenery_id,scenery_name,track_name,track_url) VALUES(?,?,?,?)'
        cur.execute(sql, track_info)
        connection.commit()

        # Update: add to history
        add_track_to_the_history(track_info)
    else:
        print("Error! cannot create database connection.")


def get_track_of_the_day():
    track_info = None
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_totd_table_if_not_exists(connection)
        cur = connection.cursor()
        cur.execute('SELECT * FROM ' + DB_TABLE_PREFIX + 'track_of_the_day')
        rows = cur.fetchall()
        if len(rows) > 1:
            print("Error! too many rows")
        print(rows)
        if rows and len(rows) == 1 and rows[0]:
            track_info = (rows[0][1], rows[0][2], rows[0][3], rows[0][4])
    else:
        print("Error! cannot create database connection.")
    return track_info


def save_leaderboard(leaderboard):
    print('save_leaderboard - leaderboard: ' + str(leaderboard))
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_leaderboard_table_if_not_exists(connection)
        cur = connection.cursor()
        cur.execute('DELETE FROM ' + DB_TABLE_PREFIX + 'leaderboard')
        connection.commit()
        json_data = json.dumps(leaderboard)
        print('save_leaderboard - json_data: ' + json_data)
        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + 'leaderboard(data)  VALUES(?)'
        cur.execute(sql, (json_data,))
        connection.commit()
    else:
        print("save_leaderboard - Error! cannot create database connection.")


# --------------------------------------------
# Leaderboard - each time something is updated
# --------------------------------------------


def get_leaderboard():
    leaderboard = None
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_leaderboard_table_if_not_exists(connection)
        cur = connection.cursor()
        cur.execute('SELECT * FROM ' + DB_TABLE_PREFIX + 'leaderboard')
        rows = cur.fetchall()
        if len(rows) > 1:
            print("Error! too many rows")
        print('get_leaderboard - rows: ' + str(rows))
        if rows:
            leaderboard = json.loads(rows[0][1])  # skip PK row
        else:
            leaderboard = []
    else:
        print("get_leaderboard - Error! cannot create database connection.")
    return leaderboard


# --------------------------------------------
# Track history - to exclude tracks that been flown recently
# --------------------------------------------


def add_track_to_the_history(track_info):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_history_table_if_not_exists(connection)
        cur = connection.cursor()
        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + 'tracks_history(scenery_name,track_name) VALUES(?,?)'
        cur.execute(sql, (track_info[1], track_info[2]))  # scenery_name + track_name
        connection.commit()
    else:
        print("Error! cannot create database connection.")


def get_tracks_history(days):
    """
    return id / date / scenery_name / track_name
    :param days:
    :return:
    """
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_history_table_if_not_exists(connection)
        cur = connection.cursor()
        sql_query = 'SELECT * FROM ' + \
                    DB_TABLE_PREFIX + 'tracks_history WHERE date >= date(\'now\', \'-' + str(days) + ' day\')'
        print('sql_query: ' + str(sql_query))
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows
    else:
        print("Error! cannot create database connection.")


# --------------------------------------------
# Daily results summary
# --------------------------------------------


def save_daily_results(daily_results):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)

        cur = connection.cursor()

        # clear all possible previous versions
        cur.execute('DELETE FROM ' + DB_TABLE_PREFIX + 'daily_results WHERE date >= date(\'now\') AND date < date(\'now\', \'+1 day\')')
        connection.commit()

        json_data = json.dumps(daily_results)
        print('save_daily_results - json_data: ' + json_data)
        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + 'daily_results(data)  VALUES(?)'
        cur.execute(sql, (json_data,))
        connection.commit()

    else:
        print("Error! cannot create database connection.")


def save_daily_results_for_day(daily_results, day_from, day_to):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)

        cur = connection.cursor()

        # clear all possible previous versions
        cur.execute('DELETE FROM ' + DB_TABLE_PREFIX + 'daily_results WHERE date >= ' + day_from + ' AND date < ' + day_to)
        connection.commit()

        json_data = json.dumps(daily_results)
        print('save_daily_results - json_data: ' + json_data)
        date_to_insert = ''
        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + 'daily_results(date, data)  VALUES(?)'
        cur.execute(sql, (date_to_insert, json_data))
        connection.commit()

    else:
        print("Error! cannot create database connection.")


def get_daily_results(previous_month=True):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)

        cur = connection.cursor()

        # because of a DST it might be 14-00 and might be 15-00 when daily_results are saved
        if previous_month:
            # 1st of the month - this is the final results day from previous month, so ignore it
            # start counting from 2nd day of month
            # but count till 1st day of current month
            sql_query = 'SELECT * FROM ' + \
                        DB_TABLE_PREFIX + 'daily_results ' + \
                        'WHERE date BETWEEN datetime(\'now\', \'-1 month\', \'start of month\', \'+1 day\', \'13 hours\', \'59 minutes\') AND ' + \
                        'datetime(\'now\', \'start of month\', \'15 hours\', \'10 minutes\')'
        else:
            # current month
            sql_query = 'SELECT * FROM ' + \
                        DB_TABLE_PREFIX + 'daily_results ' + \
                        'WHERE date BETWEEN datetime(\'now\', \'start of month\', \'+1 day\', \'13 hours\', \'59 minutes\') AND ' + \
                        'datetime(\'now\', \'+1 month\', \'start of month\',  \'15 hours\', \'10 minutes\')'

        print('get_daily_results - sql_query: ' + sql_query)
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows

    else:
        print("Error! cannot create database connection.")


def get_all_daily_results():
    """
    ID, DATE, DATA
    """
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)
        cur = connection.cursor()
        sql_query = 'SELECT * FROM ' + DB_TABLE_PREFIX + 'daily_results'
        print('get_daily_results - sql_query: ' + sql_query)
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows
    else:
        print("Error! cannot create database connection.")


def update_daily_results(id, daily_results):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)

        cur = connection.cursor()

        cur.execute('UPDATE ' + DB_TABLE_PREFIX + 'daily_results SET data=? WHERE id=?', (daily_results, id))
        connection.commit()

    else:
        print("Error! cannot create database connection.")


def get_year_daily_results(year):
    """
    ID, DATE, DATA
    """
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)
        cur = connection.cursor()
        sql_query = 'SELECT * FROM ' + DB_TABLE_PREFIX + 'daily_results WHERE date BETWEEN \'' + str(year) + \
                    '-01-01 00:00\' AND \'' + str(year+1) + '-01-01 23:59\''
        print('get_daily_results - sql_query: ' + sql_query)
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows
    else:
        print("Error! cannot create database connection.")


def get_year_monthly_results(year):
    """
    ID, DATE, DATA
    """
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)
        cur = connection.cursor()
        sql_query = 'SELECT * FROM ' + DB_TABLE_PREFIX + 'monthly_results WHERE date BETWEEN \'' + str(year) + \
                    '-01-01\' AND \'' + str(year+1) + '-01-01\''
        print('get_daily_results - sql_query: ' + sql_query)
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows
    else:
        print("Error! cannot create database connection.")


# --------------------------------------------
# All tracks for stats and analysis
# --------------------------------------------


def get_all_track_results():
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_all_tracks_table_if_not_exists(connection)
        cur = connection.cursor()
        sql_query = 'SELECT * FROM ' + DB_TABLE_PREFIX + 'all_tracks'
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows
    else:
        print("Error! cannot create database connection.")


def add_all_track_result(scenery_id, scenery_name, track_name, track_url, position, time, name, country, ranking,
                          model, date, version):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_all_tracks_table_if_not_exists(connection)
        cur = connection.cursor()

        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + 'all_tracks(scenery_id, scenery_name, track_name, track_url, ' \
                                                 'position, time, name, country, ranking, model, date, version ) ' \
                                                 ' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        # print('sql: ' + sql)
        cur.execute(sql, (scenery_id, scenery_name, track_name, track_url, position, time, name, country, ranking,
                          model, date, version))
        connection.commit()

    else:
        print("Error! cannot create database connection.")


def clear_all_track_results():
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_all_tracks_table_if_not_exists(connection)
        cur = connection.cursor()

        cur.execute('DELETE FROM ' + DB_TABLE_PREFIX + 'all_tracks')
        connection.commit()

    else:
        print("Error! cannot create database connection.")


# --------------------------------------------
# How was the track poll
# --------------------------------------------


def add_track_poll(scenery_id, scenery_name, track_name, track_url, poll_message_id, options):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_track_feedback_poll_table_if_not_exists(connection)
        cur = connection.cursor()
        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + \
              'track_feedback_poll(scenery_id,scenery_name,track_name,track_url,poll_message_id,options) VALUES(?,?,?,?,?,?)'
        params = (scenery_id, scenery_name, track_name, track_url, poll_message_id, json.dumps(options))
        cur.execute(sql, params)
        connection.commit()
    else:
        print("Error! cannot create database connection.")


def get_latest_track_poll():
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_track_feedback_poll_table_if_not_exists(connection)
        cur = connection.cursor()
        cur.execute('SELECT * FROM ' + DB_TABLE_PREFIX + 'track_feedback_poll')
        rows = cur.fetchall()
        print('all track_feedback_poll:')
        print(rows)
        if rows and len(rows) >= 1:
            sorted_latest = sorted(rows, key=lambda x: x[1], reverse=True)
            print('sorted_latest from track_feedback_poll:')
            print(sorted_latest)
            return (sorted_latest[0][0], sorted_latest[0][1], sorted_latest[0][2], sorted_latest[0][3],
                    sorted_latest[0][4], sorted_latest[0][5], sorted_latest[0][6], json.loads(sorted_latest[0][7]), )
    else:
        print("Error! cannot create database connection.")


def add_track_feedback_history(scenery_id, scenery_name, track_name, track_url, poll_message_id, rating, results):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_track_feedback_history_table_if_not_exists(connection)
        cur = connection.cursor()
        sql = 'INSERT INTO ' + DB_TABLE_PREFIX + \
              'track_feedback_history(scenery_id,scenery_name,track_name,track_url,poll_message_id,rating,results) VALUES(?,?,?,?,?,?,?)'
        params = (scenery_id, scenery_name, track_name, track_url, poll_message_id, str(rating), json.dumps(results))
        cur.execute(sql, params)
        connection.commit()
    else:
        print("Error! cannot create database connection.")


def get_all_track_feedback_history():
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_track_feedback_poll_table_if_not_exists(connection)
        cur = connection.cursor()
        cur.execute('SELECT * FROM ' + DB_TABLE_PREFIX + 'track_feedback_history')
        rows = cur.fetchall()
        return [(x[0], x[1], x[2], x[4], x[5], x[6], x[7], json.loads(x[8])) for x in rows]
    else:
        print("Error! cannot create database connection.")
