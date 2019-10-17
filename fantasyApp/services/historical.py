""" Get final stats for a given year. """
from fantasyApp.model import get_db

def getFinalStandings(league, year):
    for team in league.teams:
        teamId = team.team_id
        wins = team.wins
        losses = team.losses
        pointsFor = round(team.points_for, 1)
        standing = team.final_standing
        command = "insert into history (teamId, year, wins,\
                    losses, pointsFor, finalStanding) values \
                    (%d, %d, %d, %d, %d, %d)" % (teamId, 
                    year, wins, losses, pointsFor, standing)
        get_db().execute(command)
