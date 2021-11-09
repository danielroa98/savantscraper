from datetime import datetime
import pandas as pd
import savantscraper
import sqlite3


def create_data(dbName, seasons, mlbTeams, makeCSV):
    """ 
        Calls upon the database_import function in the savantscraper.py file.

        Args:
            dbName (str): name of the database that you want to create.
            seasons (tuple): range of years to include in the file.
            mlbTeams (list): list of teams to include in the search. If the list is empty, it will search for all the teams.
            makeCSV (bool): option to create a CSV file besides the SQLite3 database.

        Returns:
            Created SQLite3 database as well as a CSV (optional) with the data from the specified teams.
    """
    savantscraper.database_import(dbName, seasons, teams=mlbTeams, createCSV=makeCSV)

    conn = sqlite3.connect(dbName+'.db')

    df = pd.read_sql_query(
        "SELECT * FROM statcast ORDER BY game_date ASC;",
        conn)

    df['game_date'] = pd.to_datetime(df['game_date'])

    view_created_fields(df)

    if makeCSV:
        convert_to_csv(dbName)


def view_created_fields(df):
    print(df.tail())


def view_existing_data(dbName):
    conn = sqlite3.connect(dbName+'.db')

    df = pd.read_sql_query(
        "SELECT * FROM statcast ORDER BY game_date ASC, player_name DES;",
        conn)

    print(df.head())

def convert_to_csv(dbName):
    conn = sqlite3.connect(dbName+'.db')

    df = pd.read_sql_query(
        "SELECT * FROM statcast ORDER BY game_date ASC;",
        conn)

    # df.drop(index=' ')
    df.to_csv(dbName+'.csv')

if __name__ == '__main__':
    create_data('baseball_savant', (2019, 2021), ['CHC', 'NYY'], makeCSV=True)
    # convert_to_csv('baseball_savant')
    # view_existing_data('baseball_savant')
