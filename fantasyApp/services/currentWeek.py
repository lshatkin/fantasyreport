from flask_script import Manager
from fantasyApp.model import get_db
from fantasyApp.model import initialize_league
from fantasyApp import app
import statistics
import operator
# import weeklyPlayerScores as wps
# import os
# import pandas as pd
# import json



def getWeeklyInfo(league, year, week):
    total_scores = []
    scores = {}
    for matchup in league.scoreboard(week):
        scores[matchup.home_team.team_id] = round(matchup.home_score,1)
        scores[matchup.away_team.team_id] = round(matchup.away_score,1)
        total_scores.append(matchup.home_score)
        total_scores.append(matchup.away_score)
    avgScore = round(statistics.median(total_scores), 1)
    maxScore = max(scores.items(), key=operator.itemgetter(1))[1]
    maxScoreTeam = max(scores.items(), key=operator.itemgetter(1))[0]
    minScoreTeam = min(scores.items(), key=operator.itemgetter(1))[0]
    command = "insert into thisWeekSummary (week, year, topScorerId, \
                lowScorerId, averageScore, maxScore) values (%d, %d, %d, \
                %d, %d, %d)" % (week, year, maxScoreTeam, 
                minScoreTeam, avgScore, maxScore)
    get_db().execute(command)


def getTotalScoring(info):
    if CURRENT_WEEK == 1:
        info['totalScoring'] = info['scores']
        return
    with open('./data/%d/week%d/leagueInfo.json'%(YEAR,CURRENT_WEEK-1)) as json_data:
        prev_records = json.load(json_data)['totalScoring']
        json_data.close()
    for matchup in LEAGUE.scoreboard(info['previous_week']):
        prev_records[matchup.home_team.team_name] += matchup.home_score
        prev_records[matchup.away_team.team_name] += matchup.away_score
        prev_records[matchup.home_team.team_name] = round(prev_records[matchup.home_team.team_name], 1)
        prev_records[matchup.away_team.team_name] = round(prev_records[matchup.away_team.team_name], 1)
    info['totalScoring'] = OrderedDict(sorted(prev_records.items(), key=operator.itemgetter(1), reverse=True))

def rotisserie(info, dic):
    for t in LEAGUE.teams:
        t = t.team_name
        current_score = info['scores'][t]
        for o in LEAGUE.teams:
            o = o.team_name
            if o == t: continue
            opponent_score = info['scores'][o]
            if current_score > opponent_score:
                dic[t][0] += 1
            elif current_score < opponent_score:
                dic[t][1] += 1
            else:
                dic[t][2] += 1
    
    return OrderedDict(sorted(dic.items(), key=lambda e: e[1][0], reverse = True))


def rotisserieRecordWeekly(info):
    rotRecord = {t.team_name : [0,0,0] for t in LEAGUE.teams}
    info['rotisserieRecordWeekly'] = rotisserie(info, rotRecord)


def rotisserieRecordTotal(info):
    if CURRENT_WEEK == 1:
        info['rotisserieRecordTotal'] = info['rotisserieRecordWeekly']
        return
    with open('./data/%d/week%d/leagueInfo.json'%(YEAR,CURRENT_WEEK-1)) as json_data:
        prev_records = json.load(json_data)['rotisserieRecordTotal']
        json_data.close()
    info['rotisserieRecordTotal'] = rotisserie(info, prev_records)

def marginAgainstAverageWeekly(info):
    margin = {t.team_name : 0 for t in LEAGUE.teams}
    for t in LEAGUE.teams:
        t = t.team_name
        margin[t] = round(info['scores'][t] - info['average_score'], 1)
    info['marginWeekly'] = OrderedDict(sorted(margin.items(), key=operator.itemgetter(1), reverse=True))

def marginAgainstAverageTotal(info):
    if CURRENT_WEEK == 1:
        info['marginTotal'] = info['marginWeekly']
        info['marginAvg'] = info['marginWeekly']
        return
    with open('./data/%d/week%d/leagueInfo.json'%(YEAR,CURRENT_WEEK-1)) as json_data:
        prev_data = json.load(json_data)
        json_data.close()
    prev_total = prev_data['marginTotal']
    prev_avg = prev_data['marginAvg']
    for t in LEAGUE.teams:
        t = t.team_name
        marginWeekly = info['scores'][t] - info['average_score']
        prev_total[t] = round(prev_total[t]+marginWeekly, 1)
        prev_avg[t] = round(prev_total[t]/CURRENT_WEEK, 1)
    info['marginTotal'] = OrderedDict(sorted(prev_total.items(), key=operator.itemgetter(1), reverse=True))
    info['marginAvg'] = OrderedDict(sorted(prev_avg.items(), key=operator.itemgetter(1), reverse=True))
    return

def getGeneralInfo(info):
    info['previous_week'] = CURRENT_WEEK
    top_scorer = str(LEAGUE.top_scorer())
    info['top_scorer_total'] = top_scorer[top_scorer.find("(")+1:top_scorer.find(")")]
    low_scorer = str(LEAGUE.least_scorer())
    info['low_scorer_total'] = low_scorer[low_scorer.find("(")+1:low_scorer.find(")")]


def fill_config():
    info = {}
    getGeneralInfo(info)
    getScores(info)
    getTotalScoring(info)
    rotisserieRecordWeekly(info)
    rotisserieRecordTotal(info)
    marginAgainstAverageWeekly(info)
    marginAgainstAverageTotal(info)
    return info

def save(info):
    try:
        os.makedirs('./data/%d/week%d'%(YEAR, CURRENT_WEEK))
    except:
        print("Directory already created")
    with open('./data/%d/week%d/leagueInfo.json'%(YEAR,CURRENT_WEEK), 'w') as outfile:
        json.dump(info, outfile, indent = 4)


if __name__ == "__main__":

    info = fill_config()
    save(info)






