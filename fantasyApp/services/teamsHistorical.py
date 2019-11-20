""" Get final stats for a given year. """
from fantasyApp.model import get_db
import pandas as pd
import numpy as np

def getYearlyInfo(league, year):
    """ Insert necessary info into years SQL DB. """
    scores_df = createScoresDf(league)
    rot = getRotisserie(league, scores_df)
    for team in league.teams:
        t_id = team.team_id
        t_name = team.team_name.replace("'","''")
        p_for = round(team.points_for, 1)
        r_w = rot.loc[t_id, 'wins']
        r_l = rot.loc[t_id, 'losses']
        r_t = rot.loc[t_id, 'ties']
        command = "insert into years values \
                    (%d, '%s', %d, %d, %d, \
                    %d, %d, %d, %d, %d)" % (t_id,
                    t_name, year, team.wins, team.losses, 
                    p_for, team.final_standing, 
                    r_w, r_l, r_t)
        get_db().execute(command)
    r_weeks = league.settings.reg_season_count
    p_teams = league.settings.playoff_team_count
    command = "insert into yearSettings values \
                (%d, %d, %d)" % (year,
                r_weeks, p_teams)
    get_db().execute(command)

def createScoresDf(league):
    """ Create a dataframe that holds scores for all weeks. """
    reg_week_count = league.settings.reg_season_count
    reg_weeks = np.arange(1, reg_week_count + 1)
    teams = [t.team_id for t in league.teams]
    s = pd.DataFrame(index=teams, columns=reg_weeks)
    for t in league.teams:
        s.loc[t.team_id] = t.scores[0:reg_week_count]
    return s


def getRotisserie(league, scores_df):
    """ Calculate rotisserie records for a given season. """
    rot = pd.DataFrame(0, index = scores_df.index, 
            columns = ['wins', 'losses', 'ties'])
    for (week, scores) in scores_df.iteritems():
        for (t1, s1) in scores.items():
            for (t2, s2) in scores.items():
                if t1 == t2:
                    continue
                if s1 > s2:
                    rot.loc[t1, 'wins'] += 1
                elif s1 < s2:
                    rot.loc[t1, 'losses'] += 1
                elif s1 == 0 and s2 == 0:
                    continue
                else:
                    rot.loc[t1, 'ties'] += 1
    return rot
