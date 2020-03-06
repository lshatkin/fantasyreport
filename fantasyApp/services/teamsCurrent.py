""" Enter all teams into Teams DB. """
from fantasyApp.model import get_db, checkOwnership, cleanNames

def getTeams(league):
    """ Fill Teams DB. """
    for t in league.teams:
        t_id = t.team_id
        owner = checkOwnership(t.owner).replace("'","''")
        name = cleanNames(t.team_name.replace("'","''"))
        command = "insert into teams (teamId, owner, teamname)\
            values (%d, '%s', '%s')" % (t_id, owner, name)
        get_db().execute(command)
