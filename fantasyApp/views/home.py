"""
FantasyReport (Leage Home) view.

URLs include:
/<league_id>
"""

import flask
from flask import request, session, redirect, url_for
import fantasyApp
from fantasyApp.model import query_db, id_to_name, getAllYears, getAllTeams
from fantasyApp.services.badManager import badManager
from fantasyApp.services.teamOfWeek import teamOfWeek
import fantasyApp.config
import sys
import datetime
import operator
import pandas as pd


def get_top_bar_info(context):
    context['years'] = getAllYears()
    context['teams'] = getAllTeams()

def get_weekly_extras(context):
    query_weekly = "select * from thisWeekSummary"
    weekly = query_db(query_weekly,one=True)
    week = weekly['week']
    context['teamOfWeek'] = teamOfWeek(week)
    context['teamOrder'] = ['QB1', 'RB1', 'RB2', 'WR1',
                            'WR2', 'Flex', 'TE1', 
                            'D/ST1', 'K1']
    bench, start, pointDiff = badManager(week)
    context['badManBench'] = bench.to_dict()
    context['badManStart'] = start.to_dict()
    context['badManDiff'] = pointDiff
    context['badManManager'] = id_to_name(bench['team'])


def get_roto_records(context):
    query_years = "select * from years where year = %d" % context['year']
    year = query_db(query_years)
    year = pd.DataFrame.from_dict(year)
    roto = year.sort_values(by = ['rotWins'], ascending = False)
    roto = roto.loc[:, ['teamId', 'rotWins', 'rotLosses']]
    teamNameConversion = lambda x : id_to_name(x)
    roto['teamName'] = roto['teamId'].apply(teamNameConversion)
    context['roto'] = roto


def get_weekly_info(context):
    query_weekly = "select * from thisWeekSummary"
    weekly = query_db(query_weekly,one=True)
    context['weekly_info']['top_scorer'] = id_to_name(weekly['topScorerId'])
    context['weekly_info']["top_score"] = weekly['maxScore']
    context['weekly_info']['avg_score'] = weekly['averageScore']
    context['weekly_info']['low_scorer'] = id_to_name(weekly['lowScorerId'])
    context['weekly_info']["low_score"] = weekly['minScore']
    context['week'] = weekly['week']
    context['year'] = datetime.datetime.now().year
    query_years = "select * from years where year = %d" % context['year']
    points = query_db(query_years)
    pointsDf = pd.DataFrame.from_dict(points)
    max_points = max(pointsDf['pointsFor'])
    min_points = min(pointsDf['pointsFor'])
    id_max = pointsDf.loc[pointsDf['pointsFor'].idxmax()]['teamId']
    id_min = pointsDf.loc[pointsDf['pointsFor'].idxmin()]['teamId']
    context['weekly_info']['max_score_team'] = id_to_name(id_max)
    context['weekly_info']['max_score'] = max_points
    context['weekly_info']['min_score_team'] = id_to_name(id_min)
    context['weekly_info']['min_score'] = min_points
    return context


def get_reigning_champ(context):
    query_champ = "select * from years where year = %d" % (context['year'] - 1)
    champ = query_db(query_champ)
    for team in champ:
        if team['finalStanding'] == 1:
            context['current_champion'] = id_to_name(team['teamId'])


def get_standings(context):
    query_teams = "select * from years where year = %d" % context['year']
    teams = pd.DataFrame.from_dict(query_db(query_teams))
    standings = teams.sort_values(by = ['wins', 'pointsFor'], ascending = False)
    standings = standings.loc[:, ['teamId', 'wins', 'losses']]
    teamNameConversion = lambda x : id_to_name(x)
    standings['teamName'] = standings['teamId'].apply(teamNameConversion)
    context['standings'] = standings


@fantasyApp.app.route('/', methods=['GET'])
def show_home():
    """Display / route."""
    context = {"weekly_info": {},
                "standings": {},
                "rotisserie": {},
                "avg_margin": {},
    }
    get_top_bar_info(context)
    get_weekly_info(context)
    get_reigning_champ(context)
    get_standings(context)
    get_weekly_extras(context)
    get_roto_records(context)
    return flask.render_template("home.html", **context)

    #print('###########', file=sys.stderr)
    #print(context['standings'], file=sys.stderr)
    #print('###########', file=sys.stderr)
