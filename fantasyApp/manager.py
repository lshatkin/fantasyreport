from flask_script import Manager
from fantasyApp.services.historical import getYearlyInfo, getRotisserie
from fantasyApp.services.teams import getTeams
import fantasyApp.services.currentWeek as currentWeek
from fantasyApp.services.players import addPlayersToDB, addPlayerInfo
from fantasyApp.model import initialize_league
from fantasyApp import app

manager = Manager(app)
currentLeague = initialize_league(2019)

# @manager.command
# def fillHistoricalDBs():
#     for year in range(2014, 2020):
#         print(year)
#         l = initialize_league(year)
#         getYearlyInfo(l, year)
#     getTeams(currentLeague)

@manager.command
def fillCurrentDBs():
    """ Get information from current week. """
    week = currentLeague.current_week - 1
    currentWeek.getWeeklyInfo(currentLeague, 2019, week)
    addPlayersToDB(currentLeague, week)
    addPlayerInfo(currentLeague, week)


if __name__ == "__main__":
    manager.run()