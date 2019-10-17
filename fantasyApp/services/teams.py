""" Enter all teams into Teams DB. """
from fantasyApp.model import get_db, checkOwnership

def getTeams(league):
    """ Fill Teams DB. """
    for t in league.teams:
        teamId = t.team_id
        owner = checkOwnership(t.owner).replace("'","''")
        name = t.team_name.replace("'","''")
        command = "insert into teams (teamId, owner, teamname)\
            values (%d, '%s', '%s')" % (teamId, owner, name)
        get_db().execute(command)
