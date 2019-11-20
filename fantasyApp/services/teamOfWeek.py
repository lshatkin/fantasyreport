"""Calculate the team of the week."""
import pandas as pd
import numpy as np
from fantasyApp.model import id_to_name
from fantasyApp.services.players import createPlayersDf


def teamOfWeek(week):
    """ Identify team of the week. """
    df = createPlayersDf(week)
    convertName = lambda x : id_to_name(x)
    df['teamName'] = df['team'].apply(convertName)
    team = {}
    numSpots = {'QB' : 1, 'RB' : 2, 
                'WR' : 2, 'TE' : 1,
                'D/ST' : 1, 'K' : 1}
    flex_spots = ['WR', 'RB', 'TE']
    flex_points = 0
    for pos in df.position.unique():
        df = df.sort_values(by = ['points'], 
                ascending = False)
        top = df.loc[df['position'] == pos]
        numPlayers = numSpots[pos]
        for i in range(numPlayers):
            p = top.iloc[i]
            pInfo = [p['name'], p['points'], 
                    p['team'], p['teamName']]
            team[pos+str(i+1)] = pInfo
        if pos in flex_spots:
            f = top.iloc[numPlayers]
            if f['points'] > flex_points:
                pInfo = [f['name'], f['points'], 
                        f['team'], f['teamName']]
                team['Flex'] = pInfo
                flex_points = f['points']
    return team