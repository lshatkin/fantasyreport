""" Get the bad manager of the week """
from fantasyApp.services.players import createPlayersDf
import pandas as pd
import numpy as np

def badManager(week):
    """ Identify the bad manager of the week. """
    df = createPlayersDf(week)
    positions = ['RB', 'QB', 'WR', 'RB/WR/TE']
    l_points = 0
    b_player, s_player = 0, 0
    for t in df.team.unique():
        rost = df.loc[df['team'] == t]
        s_p = rost.loc[rost['slot'] != 'BE']
        b_p = rost.loc[rost['slot'] == 'BE']
        for p in positions:
            s = s_p.loc[s_p['slot']==p]
            if p == 'RB/WR/TE':
                flex_pos = ['WR', 'RB', 'TE']
                b = b_p.loc[b_p['position'].isin(flex_pos)]
            else:
                b = b_p.loc[b_p['position'] == p]
            if len(b) == 0:
                continue
            min_s = s.loc[s['points'].idxmin()]
            max_b = b.loc[b['points'].idxmax()]
            if (max_b['points'] - min_s['points']) > l_points:
                l_points = max_b['points'] - min_s['points']
                b_player = max_b
                s_player = min_s
    return b_player, s_player, l_points