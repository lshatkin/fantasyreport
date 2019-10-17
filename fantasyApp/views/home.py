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


def id_to_name(id):
    query_team = "select * from teams where teamId = %d" % id
    name = query_db(query_team, one=True)['teamName']
    return name


def get_weekly_info():
    context = {"weekly_info": {},
                "current_champion": "",
                "standings": {},
                "rotisserie": {},
                "avg_margin": {},
                "week": 0,
                "year": 0
                }

    query_weekly = "select * from thisWeekSummary"
    weekly = query_db(query_weekly,one=True)
    context['weekly_info']['top_scorer'] = id_to_name(weekly['topScorerId'])
    context['weekly_info']["top_score"] = weekly['maxScore']
    context['weekly_info']['avg_score'] = weekly['averageScore']
    context['week'] = weekly['week']
    context['year'] = datetime.datetime.now().year
    query_years = "select * from years where year = %d" % context['year']
    points = query_db(query_years)
    max_points = 0
    id_max = 0
    min_points = points[0]['pointsFor']
    id_min = 0
    for team in points:
        if team['pointsFor'] > max_points:
            max_points = team['pointsFor']
            id_max = team['teamId']
        if team['pointsFor'] < min_points:
            min_points = team['pointsFor']
            id_min = team['teamId']
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
        context['standings'][id_to_name(team['teamId'])] = f"{team['wins']}-{team['losses']}-0"
        #context['standings'] = sorted(context['standings'].items(), key=lambda x: x[1], reverse=True)

    #print('###########', file=sys.stderr)
    #print(context['standings'], file=sys.stderr)
    #print('###########', file=sys.stderr)




@fantasyApp.app.route('/', methods=['GET'])
def show_home():
    """Display / route."""
    context = get_weekly_info()
    get_reigning_champ(context)
    get_standings(context)



    return flask.render_template("home.html", **context)
