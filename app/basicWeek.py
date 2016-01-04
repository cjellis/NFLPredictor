from __future__ import division
import common
import json
from flask import Blueprint

#####################################################################
# Blueprint for Flask
basic = Blueprint('basic', __name__, url_prefix='/basic')

#####################################################################
# Global Variables
weeks = {}

records = {
    'IND': {'win': 0, 'loss': 0},
    'HOU': {'win': 0, 'loss': 0},
    'SEA': {'win': 0, 'loss': 0},
    'CIN': {'win': 0, 'loss': 0},
    'BUF': {'win': 0, 'loss': 0},
    'TEN': {'win': 0, 'loss': 0},
    'CHI': {'win': 0, 'loss': 0},
    'KCC': {'win': 0, 'loss': 0},
    'NOS': {'win': 0, 'loss': 0},
    'PHI': {'win': 0, 'loss': 0},
    'STL': {'win': 0, 'loss': 0},
    'GBP': {'win': 0, 'loss': 0},
    'JAC': {'win': 0, 'loss': 0},
    'TBB': {'win': 0, 'loss': 0},
    'WAS': {'win': 0, 'loss': 0},
    'ATL': {'win': 0, 'loss': 0},
    'CLE': {'win': 0, 'loss': 0},
    'BAL': {'win': 0, 'loss': 0},
    'ARI': {'win': 0, 'loss': 0},
    'DET': {'win': 0, 'loss': 0},
    'DEN': {'win': 0, 'loss': 0},
    'OAK': {'win': 0, 'loss': 0},
    'NEP': {'win': 0, 'loss': 0},
    'DAL': {'win': 0, 'loss': 0},
    'SFO': {'win': 0, 'loss': 0},
    'NYG': {'win': 0, 'loss': 0},
    'PIT': {'win': 0, 'loss': 0},
    'SDG': {'win': 0, 'loss': 0},
    'NYJ': {'win': 0, 'loss': 0},
    'MIA': {'win': 0, 'loss': 0},
    'MIN': {'win': 0, 'loss': 0},
    'CAR': {'win': 0, 'loss': 0}
}

division_standings = []
playoffs = []

#####################################################################
# Internal Functions


def determine_winner_and_update_record(game, string):
    home = game['home']
    away = game['visitor']
    home_team_abbr = common.mapping.get(home)
    away_team_abbr = common.mapping.get(away)
    home_team_record = records.get(home_team_abbr)
    away_team_record = records.get(away_team_abbr)
    away_total = away_team_record['loss'] + away_team_record['win']
    home_total = home_team_record['loss'] + home_team_record['win']
    away_percent = 0 if away_total is 0 else away_team_record['win'] / away_total
    home_percent = 0 if home_total is 0 else home_team_record['win'] / home_total

    if away_percent > home_percent:
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div>".format(away, home, away)
        records[home_team_abbr]['loss'] += 1
        records[away_team_abbr]['win'] += 1
    else:
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div>".format(away, home, home)
        records[away_team_abbr]['loss'] += 1
        records[home_team_abbr]['win'] += 1
    return string


def determine_winners(week_number, games, string):
    string += "<div><h3>{0}</h3></div>".format(week_number)
    string += "<table>"
    i = 0
    for game in games:
        if i == 0:
            string += "<tr><td>"
        if i == 1:
            string += "</td><td>"
        string = determine_winner_and_update_record(game, string)
        i += 1
        if i == 2:
            string += "</td></tr>"
            i = 0
    string += "</table>"
    return string


def predict_games(uptoweek, endweek, string):
    global schedule, records, division_standings
    schedule = common.schedule

    games = common.get_games(uptoweek)

    records = common.update_records(games, records, uptoweek)

    i = uptoweek
    while i <= endweek:
        week = "WEEK {0}".format(i)
        gamestoplay = schedule.get(week)
        string = determine_winners(week, gamestoplay, string)
        division_standings = common.update_division_records(records)
        string = common.print_records_by_div(string, division_standings)
        i += 1

    return string


#####################################################################
# API Endpoints
@basic.route('/guessWeek/<week_to_predict>', methods=['GET'])
def run(week_to_predict):
    global records
    records = common.reset_records(records)
    string = common.set_up_html_string()
    string = predict_games(int(week_to_predict), int(week_to_predict), string)
    return json.dumps({'data': common.finish_html_string(string)}, 200, {'ContentType': 'application/json'})


# currently not used from the front end
@basic.route('/guessFromWeek/<week_to_predict>', methods=['GET'])
def guess_from_week(week_to_predict):
    global records
    records = common.reset_records(records)
    string = common.set_up_html_string()
    string = predict_games(int(week_to_predict), 17, string)
    return common.finish_html_string(string)
