from flask_script import Manager
from fantasyApp.model import get_db
from fantasyApp.model import initialize_league
from fantasyApp import app
import numpy as np
import pandas as pd
import statistics
import operator

def createScoresWeek(league, week):
    """ Create a dataframe that holds scores for all weeks. """
    regSeasonWeeks = np.arange(1, league.settings.reg_season_count + 1)
    teams = [t.team_id for t in league.teams]
    scoring = pd.DataFrame(index = teams, columns = regSeasonWeeks)
    for t in league.teams:
        scoring.loc[t.team_id] = t.scores[0:league.settings.reg_season_count]
    return scoring.loc[:, week]


def weeklyAwards(scoresDf, year, week):
    """ Calculate weekly awards for homepage. """
    maxScore = scoresDf.max()
    indexMax = scoresDf.values.argmax()
    maxScoreTeam = scoresDf.index[indexMax]
    indexMin = scoresDf.values.argmin()
    minScoreTeam = scoresDf.index[indexMin]
    median = scoresDf.median()
    command = "insert into thisWeekSummary values (%d, %d, %d, \
                %d, %d, %d)" % (week, year, maxScoreTeam, 
                minScoreTeam, median, maxScore)
    get_db().execute(command)


def fillThisWeekScores(scoresDf):
    """ Fill in weekly scores DB. """
    for i in scoresDf.index:
        score = scoresDf.loc[i]
        command = "insert into thisWeekScores values \
                    (%d, %d)" % (i, score)
        get_db().execute(command)


def getWeeklyInfo(league, year, week):
    """ Get general weekly for display on homepage. """
    scoresDf = createScoresWeek(league, week)
    weeklyAwards(scoresDf, year, week)
    fillThisWeekScores(scoresDf)
