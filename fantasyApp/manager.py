from flask_script import Manager
from fantasyApp.services.historical import getFinalStandings
from fantasyApp.services.teams import getTeams
from fantasyApp.model import initialize_league
from fantasyApp import app

manager = Manager(app)

@manager.command
def fillDBs():
    currentLeague = initialize_league(2019)
    for year in range(2014, 2019):
        l = initialize_league(year)
        getFinalStandings(l, year)
    getTeams(currentLeague)


if __name__ == "__main__":
    manager.run()