"""
FantasyReport (Leage Home) view.

URLs include:
/<league_id>
"""

import flask
from flask import request, session, redirect, url_for
import fantasyApp
from fantasyApp.model import query_db
import fantasyApp.config
import sys
import datetime
import operator
import pandas as pd


def id_to_name(id):
    query_team = "select * from teams where teamId = %d" % id
    name = query_db(query_team, one=True)['teamName']
    return name


def get_weekly_info(context):
    query_weekly = "select * from thisWeekSummary"
    weekly = query_db(query_weekly,one=True)
    context['weekly_info']['top_scorer'] = id_to_name(weekly['topScorerId'])
    context['weekly_info']["top_score"] = weekly['maxScore']
    context['weekly_info']['avg_score'] = weekly['averageScore']
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
    teams = query_db(query_teams)
    for team in teams:
        context['standings'][id_to_name(team['teamId'])] = f"{team['wins']}-{team['losses']}"
        #context['standings'] = sorted(context['standings'].items(), key=lambda x: x[1], reverse=True)


@fantasyApp.app.route('/', methods=['GET'])
def show_home():
    """Display / route."""
    context = {"weekly_info": {},
                "current_champion": "",
                "standings": {},
                "rotisserie": {},
                "avg_margin": {},
                "week": 0,
                "year": 0
    }
    get_weekly_info(context)
    get_reigning_champ(context)
    get_standings(context)
    return flask.render_template("home.html", **context)

    #print('###########', file=sys.stderr)
    #print(context['standings'], file=sys.stderr)
    #print('###########', file=sys.stderr)
