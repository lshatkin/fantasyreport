""" Get final stats for a given year. """
from fantasyApp.model import get_db, query_db, id_to_name
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
    for matchup in league.box_scores(week):
        for p in matchup.home_lineup:
            executeAdd(p, matchup.home_team.team_id)
        for p in matchup.away_lineup:
            executeAdd(p, matchup.away_team.team_id)


def createPlayersDf(week):
    """ Get all the players on a lineup this week. """
    query = "select * from players"
    players = query_db(query)
    return pd.DataFrame.from_dict(players)


def badManager(week):
    """ Identify the bad manager of the week. """
    df = createPlayersDf(week)
    positions = ['RB', 'QB', 'WR', 'RB/WR/TE']
    leftPoints = 0
    benchPlayer, startPlayer = 0, 0
    for t in df.team.unique():
        roster = df.loc[df['team'] == t]
        starters = roster.loc[roster['slot'] != 'BE']
        bench = roster.loc[roster['slot'] == 'BE']
        for p in positions:
            s = starters.loc[starters['slot']==p]
            if p == 'RB/WR/TE':
                b = bench.loc[bench['position'].isin(['WR', 'RB', 'TE'])]
            else:
                b = bench.loc[bench['position'] == p]
            if len(b) == 0:
                continue
            minStart = s.loc[s['points'].idxmin()]
            maxBench = b.loc[b['points'].idxmax()]
            if (maxBench['points'] - minStart['points']) > leftPoints:
                leftPoints = maxBench['points'] - minStart['points']
                benchPlayer = maxBench
                startPlayer = minStart
    return benchPlayer, startPlayer, leftPoints


def teamOfWeek(week):
    """ Identify team of the week. """
    df = createPlayersDf(week)
    teamNameConversion = lambda x : id_to_name(x)
    df['teamName'] = df['team'].apply(teamNameConversion)
    team = {}
    numSpots = {'QB' : 1, 'RB' : 2, 
                'WR' : 2, 'TE' : 1,
                'D/ST' : 1, 'K' : 1}
    flex_spots = ['WR', 'RB', 'TE']
    flex_points = 0
    for pos in df.position.unique():
        df = df.sort_values(by = ['points'], ascending = False)
        top = df.loc[df['position'] == pos]
        numPlayers = numSpots[pos]
        for i in range(numPlayers):
            p = top.iloc[i]
            pInfo = [p['name'], p['points'], p['team'], p['teamName']]
            team[pos+str(i+1)] = pInfo
        if pos in flex_spots:
            f = top.iloc[numPlayers]
            if f['points'] > flex_points:
                pInfo = [f['name'], f['points'], f['team'], f['teamName']]
                team['Flex'] = pInfo
                flex_points = f['points']
    return team
