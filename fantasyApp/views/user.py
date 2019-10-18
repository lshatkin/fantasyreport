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


def get_basic_info(context, teamId):
    query_years = "select * from years where teamId = %d" % teamId
    teamHistory = query_db(query_years)
    teamHistoryDf = pd.DataFrame.from_dict(teamHistory)
    context['totalWins'] = teamHistoryDf['wins'].sum()
    context['totalLosses'] = teamHistoryDf['losses'].sum()
    context['totalRotWins'] = teamHistoryDf['rotWins'].sum()
    context['totalRotLosses'] = teamHistoryDf['rotLosses'].sum()
    print(context, file=sys.stderr)


@fantasyApp.app.route('/u/<team_id>/', methods=['GET'])
def show_user(team_id):
    """Display / route."""
    teamId = int(team_id)
    context = {}   
    get_top_bar_info(context)
    get_name(context, teamId)
    get_basic_info(context, teamId)
    return flask.render_template("user.html", **context)
