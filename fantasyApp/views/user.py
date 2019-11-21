"""
FantasyReport (Leage Home) view.

URLs include:
/<team_id>
"""
import flask
import fantasyApp
from fantasyApp.model import query_db, id_to_name, getAllYears, getAllTeams, id_to_owner
import fantasyApp.config
import sys
import pandas as pd


def get_top_bar_info(context):
    context['years'] = getAllYears()
    context['teams'] = getAllTeams()


def get_name(context, teamId):
    context['teamName'] = id_to_name(teamId)
    context['owner'] = id_to_owner(teamId)


def get_best_year(context, teamId):
    query_years = "select * from years where teamId = %d" % teamId
    teamHistory = query_db(query_years)
    teamHistoryDf = pd.DataFrame.from_dict(teamHistory)
    bestYear = teamHistoryDf.loc[teamHistoryDf['wins'] == max(teamHistoryDf['wins'])]
    context['bestYearWins'] = int(bestYear.iloc[0]['wins'])
    context['bestYearLosses'] = int(bestYear.iloc[0]['losses'])
    context['bestYearFinalStanding'] = int(bestYear.iloc[0]['finalStanding'])
    context['bestYear'] = int(bestYear.iloc[0]['year'])

def get_historical_rosters(context, teamId):
    query_rosters = "select * from historicalRosters where teamId = %d" % teamId
    rosters = pd.DataFrame.from_dict(query_db(query_rosters))
    rosters = rosters.sort_values(by = ['year'], ascending = False)
    roster_players = rosters.iloc[:, 2:].set_index(rosters['year'])
    context['roster_players'] = roster_players.T
    

def get_basic_info(context, teamId):
    query_years = "select * from years where teamId = %d" % teamId
    teamHistory = query_db(query_years)
    teamHistoryDf = pd.DataFrame.from_dict(teamHistory)
    context['totalWins'] = teamHistoryDf['wins'].sum()
    context['totalLosses'] = teamHistoryDf['losses'].sum()
    context['totalRotWins'] = teamHistoryDf['rotWins'].sum()
    context['totalRotLosses'] = teamHistoryDf['rotLosses'].sum()
    context['championships'] = len(teamHistoryDf[teamHistoryDf['finalStanding'] == 1])
    context['rotWins'] = teamHistoryDf['rotWins'].sum()
    context['rotLosses'] = teamHistoryDf['rotLosses'].sum()
    currentYear = teamHistoryDf.loc[teamHistoryDf['year'] == max(teamHistoryDf['year'])]
    context['currentWins'] = int(currentYear.iloc[0]['wins'])
    context['currentLosses'] = int(currentYear.iloc[0]['losses'])   
    context['teamHistory'] = teamHistoryDf.sort_values(by = ['year'])


@fantasyApp.app.route('/u/<team_id>/', methods=['GET'])
def show_user(team_id):
    """Display / route."""
    teamId = int(team_id)
    context = {}   
    get_historical_rosters(context, teamId)
    get_top_bar_info(context)
    get_name(context, teamId)
    get_basic_info(context, teamId)
    get_best_year(context, teamId)
    return flask.render_template("user.html", **context)
