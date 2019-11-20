""" Get final stats for a given year. """
from fantasyApp.model import get_db, query_db
import pandas as pd
import numpy as np

def executeAdd(p, team_id):
    """ Add players to SQL DB. """
    name = p.name.replace("'", "''")
    command = "insert into players values ('%s', \
        %d, %d, '%s', '%s', %d)" % (name,
        p.points, p.projected_points,
        p.position, p.slot_position, 
        team_id)
    get_db().execute(command)


def addPlayersToDB(league, week):
    """ Get all the players on a lineup this week. """
    for m in league.box_scores(week):
        for p in m.home_lineup:
            executeAdd(p, m.home_team.team_id)
        for p in m.away_lineup:
            executeAdd(p, m.away_team.team_id)


def createPlayersDf(week):
    """ Get all the players on a lineup this week. """
    query = "select * from players"
    players = query_db(query)
    return pd.DataFrame.from_dict(players)
