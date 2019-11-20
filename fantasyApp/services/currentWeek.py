from flask_script import Manager
from fantasyApp.model import get_db
from fantasyApp.model import initialize_league
from fantasyApp import app
import numpy as np
import pandas as pd
import statistics
import operator


def createScoresDf(league, week):
    """ Create a dataframe that holds scores. """
    num_w = league.settings.reg_season_count
    reg_weeks = np.arange(1, num_w+1)
    teams = [t.team_id for t in league.teams]
    s = pd.DataFrame(index=teams, columns=reg_weeks)
    for t in league.teams:
        s.loc[t.team_id] = t.scores[0:num_w]
    return s.loc[:, week]


def weeklyAwards(scores_df, year, week):
    """ Calculate weekly awards for homepage. """
    i_max = scores_df.values.argmax()
    max_team = scores_df.index[i_max]
    i_min = scores_df.values.argmin()
    min_team = scores_df.index[i_min]
    command = "insert into thisWeekSummary values (%d, \
                %d, %d, %d, %d, %d, \
                %d)" % (week, year, max_team, 
                min_team, scores_df.median(), 
                scores_df.max(), scores_df.min())
    get_db().execute(command)


def fillScores(scores_df):
    """ Fill in weekly scores DB. """
    for i in scores_df.index:
        score = scores_df.loc[i]
        command = "insert into thisWeekScores \
                    values (%d, %d)" % (i, score)
        get_db().execute(command)


def getWeeklyInfo(league, year, week):
    """ Get general weekly for display on homepage. """
    scores_df = createScoresDf(league, week)
    weeklyAwards(scores_df, year, week)
    fillScores(scores_df)
