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


def get_information():
    context = {"weekly_info": {},
                "current_champion": "",
                "standings": {},
                "rotisserie": {},
                "avg_margin": {},
                "week": ""
                }

    query_weekly = "select * from thisWeekSummary"
    weekly = query_db(query_weekly,one=True)
    query_team = "select * from teams where teamId = '%s'" % weekly['topScorerId']
    context['weekly_info']['top_scorer'] = query_db(query_team, one=True)['teamName']
    context['weekly_info']["max_score"] = weekly['maxScore']
    context['weekly_info']['avg_score'] = weekly['averageScore']
    context['week'] = weekly['week']

    #print('###########', file=sys.stderr)
    #print(context['weekly_info']['top_scorer'], file=sys.stderr)
    #print('###########', file=sys.stderr)

    return context




@fantasyApp.app.route('/', methods=['GET'])
def show_home():
    """Display / route."""
    context = get_information()

    return flask.render_template("home.html", **context)
