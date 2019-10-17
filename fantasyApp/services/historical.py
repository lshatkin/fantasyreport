""" Get final stats for a given year. """
from fantasyApp.model import get_db
import pandas as pd
import numpy as np

def getYearlyInfo(league, year):
    """ Insert necessary info into years SQL DB. """
    scoresDf = createScoresDf(league)
    rotRecords = getRotisserie(league, scoresDf)
    for team in league.teams:
        teamId = team.team_id
        wins = team.wins
        losses = team.losses
        pointsFor = round(team.points_for, 1)
        standing = team.final_standing
        rotWins = rotRecords.loc[teamId, 'wins']
        rotLosses = rotRecords.loc[teamId, 'losses']
        rotTies = rotRecords.loc[teamId, 'ties']
        command = "insert into years values \
                    (%d, %d, %d, %d, %d, %d, %d, %d, %d)" % (teamId,
                    year, wins, losses, 
                        pointsFor, standing, rotWins, rotLosses, rotTies)
        get_db().execute(command)

def createScoresDf(league):
    """ Create a dataframe that holds scores for all weeks. """
    regSeasonWeeks = np.arange(1, league.settings.reg_season_count + 1)
    teams = [t.team_id for t in league.teams]
    scoring = pd.DataFrame(index = teams, columns = regSeasonWeeks)
    for t in league.teams:
        scoring.loc[t.team_id] = t.scores[0:league.settings.reg_season_count]
    return scoring


def getRotisserie(league, scoresDf):
    """ Calculate rotisserie records for a given season. """
    rot = pd.DataFrame(0, index = scoresDf.index, columns = ['wins', 'losses', 'ties'])
    for (week, scores) in scoresDf.iteritems():
        for (teamId1, s1) in scores.items():
            for (teamId2, s2) in scores.items():
                if teamId1 == teamId2:
                    continue
                if s1 > s2:
                    rot.loc[teamId1, 'wins'] += 1
                elif s1 < s2:
                    rot.loc[teamId1, 'losses'] += 1
                elif s1 == 0 and s2 == 0:
                    continue
                else:
                    rot.loc[teamId1, 'ties'] += 1
    return rot
