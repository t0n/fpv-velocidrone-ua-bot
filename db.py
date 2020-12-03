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


def get_daily_results(previous_month=True):
    connection = _create_connection(DB_FILE)
    if connection is not None:
        _create_daily_results_table_if_not_exists(connection)

        cur = connection.cursor()

        if previous_month:
            # 1st of the month - this is the final results day from previous month, so ignore it
            # start counting from 2nd day of month
            # but count till 1st day of current month
            sql_query = 'SELECT * FROM ' + \
                        DB_TABLE_PREFIX + 'daily_results ' + \
                        'WHERE date BETWEEN date(\'now\', \'-1 month\', \'start of month\', \'+1 day\', \'15 hours\', \'5 minutes\') AND ' + \
                        'date(\'now\', \'start of month\', \'15 hours\', \'5 minutes\')'
        else:
            # current month
            sql_query = 'SELECT * FROM ' + \
                        DB_TABLE_PREFIX + 'daily_results ' + \
                        'WHERE date BETWEEN date(\'now\', \'start of month\', \'+1 day\', \'15 hours\', \'5 minutes\') AND ' + \
                        'date(\'now\', \'+1 month\', \'start of month\',  \'15 hours\', \'5 minutes\')'

        print('get_daily_results - sql_query: ' + sql_query)
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows

    else:
        print("Error! cannot create database connection.")
