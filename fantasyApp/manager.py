from flask_script import Manager
from fantasyApp.services.teamsHistorical import getYearlyInfo, getRotisserie
from fantasyApp.services.teamsCurrent import getTeams
from fantasyApp.services.currentWeek import getWeeklyInfo
from fantasyApp.services.playersCurrent import addPlayersToDB
from fantasyApp.model import initialize_league
from fantasyApp import app
from tqdm import tqdm

manager = Manager(app)
currentLeague = initialize_league(2019)

@manager.command
def fillHistoricalDBs():
    for year in tqdm(range(2015, 2020)):
        l = initialize_league(year)
        getYearlyInfo(l, year)
    getTeams(currentLeague)

@manager.command
def fillCurrentDBs():
    """Get information from current week."""
    week = currentLeague.current_week - 1
    week = 12
    getWeeklyInfo(currentLeague, 2019, week)
    addPlayersToDB(currentLeague, week)

@manager.command
def test():
    for t in currentLeague.teams:
        roster = t.roster
        for player in roster:
            print(player.name, player.posRank)


if __name__ == "__main__":
    manager.run()