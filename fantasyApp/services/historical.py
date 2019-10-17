from ff_espn_api import League
import json
import os
from fantasyApp.model import checkOwnership, get_db

def initialize_league(year):
    API_INFO = {
        'league_id' : 428926,
        'year' : year,
        'swid' : '{E176D073-7C0F-4936-9728-43E7ABFE1AB7}',
        'espn_s2' : 'AEBrMaWPzGMPhFTsowo%2FITsrbK8AYrSqSZ2Hkb%2BAZgMkMw1uxafrpn3YN2fLyok5Z%2FekNw%2F8yvZ8xtXVIqrAGDD8wQbY1yUi1ygqUrtlB%2FcNpIDc9AgTS2ZHXriAAE69g%2B3zeLdXfhCu9ioMvMYmSp8EHLU0r%2FyJCi3Dj0%2BPIoL8QJGGD4awqXX0uYtltTQ9uEBI9itLcgTph9evvEf%2Bto1yPjN%2FljtBM%2FIuJ4ci3vzqsO8Op2kKbxVb6C3TW%2BLHOW2AtIiI9j9BAqlrgzqrwGTBs5bd%2FAjyDTvQ1Qrxd8uzDw%3D%3D'
    }
    return League(API_INFO['league_id'], 
                        API_INFO['year'], 
                        API_INFO['espn_s2'], 
                        API_INFO['swid'])


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
    


def getInfo():
    for year in range(2014, 2019):
        l = initialize_league(year)
        getFinalStandings(l, year)


