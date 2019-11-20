"""Insta485 model (database) API."""
import sqlite3
import flask
from fantasyApp import app
from ff_espn_api import League
import pandas as pd

def checkOwnership(owner):
    """ Change owner names - hard coded. """
    if owner == 'Sam Spiwak' or owner == 'Ethan S':
        return 'Spiwak and Schnoll'
    if owner == 'Jack Kremin' or owner == 'Eli O':
        return 'Eli and Krem'
    if owner == 'Jim O\'Donnell':
        return 'Sam O\'Donnell'
    return owner


def id_to_name(id):
    """ Convert a team id into a team name. """
    query_team = "select * from teams where teamId = %d" % id
    name = query_db(query_team, one=True)['teamName']
    return name

def id_to_owner(id):
    """ Convert a team id into a team owner. """
    query_team = "select * from teams where teamId = %d" % id
    owner = query_db(query_team, one=True)['owner']
    return owner


def getAllYears():
    """ Get years for top bar, needed on every page. """
    query_years = "select year from years"
    years = query_db(query_years)
    uniqueYears = pd.DataFrame(years)['year'].unique()
    return uniqueYears


def getAllTeams():
    query_team = "select teamId, teamName from teams"
    name = query_db(query_team)
    return name


def initialize_league(year):
    """ Initialize league, needed in most scripts. """
    API_INFO = {
        'league_id' : 428926,
        'year' : year,
        'swid' : '{E176D073-7C0F-4936-9728-43E7ABFE1AB7}',
        'espn_s2' : 'AEBrMaWPzGMPhFTsowo%2FITsrbK8AYrSqSZ2Hkb%2BAZgMkMw1uxafrpn3YN2fLyok5Z%2FekNw%2F8yvZ8xtXVIqrAGDD8wQbY1yUi1ygqUrtlB%2FcNpIDc9AgTS2ZHXriAAE69g%2B3zeLdXfhCu9ioMvMYmSp8EHLU0r%2FyJCi3Dj0%2BPIoL8QJGGD4awqXX0uYtltTQ9uEBI9itLcgTph9evvEf%2Bto1yPjN%2FljtBM%2FIuJ4ci3vzqsO8Op2kKbxVb6C3TW%2BLHOW2AtIiI9j9BAqlrgzqrwGTBs5bd%2FAjyDTvQ1Qrxd8uzDw%3D%3D'
    }
    return League(API_INFO['league_id'],
                        API_INFO['year'],
                        API_INFO['espn_s2'],
                        API_INFO['swid'])

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary."""
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def query_db(query, args=(), one=False):
    """Query from the database."""
    cur = get_db().execute(query, args)
    r_v = cur.fetchall()
    cur.close()
    return (r_v[0] if r_v else None) if one else r_v


def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")
    return flask.g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request."""
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()
