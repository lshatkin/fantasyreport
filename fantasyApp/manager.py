from flask_script import Manager
from fantasyApp.services.historical import getYearlyInfo, getRotisserie
from fantasyApp.services.teams import getTeams
import fantasyApp.services.currentWeek as currentWeek
from fantasyApp.model import initialize_league
from fantasyApp import app

manager = Manager(app)
currentLeague = initialize_league(2019)

@manager.command
def fillHistoricalDBs():
    for year in range(2014, 2020):
        print(year)
        l = initialize_league(year)
        getYearlyInfo(l, year)
    getTeams(currentLeague)

@manager.command
def fillCurrentDBs():
    currentWeek.getWeeklyInfo(currentLeague, 2019, 5)


if __name__ == "__main__":
    manager.run()