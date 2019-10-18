"""
FantasyReport (Leage Home) view.

URLs include:
/<team_id>
"""
import flask
import fantasyApp
from fantasyApp.model import query_db, id_to_name, getAllYears, getAllTeams
import fantasyApp.config


def get_top_bar_info(context):
    context['years'] = getAllYears()
    context['teams'] = getAllTeams()


@fantasyApp.app.route('/u/<team_id>/', methods=['GET'])
def show_user(team_id):
    """Display / route."""
    context = {}
    context['teamName'] = id_to_name(int(team_id))
    get_top_bar_info(context)
    return flask.render_template("user.html", **context)
