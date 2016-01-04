from __future__ import division
import nflgame
import common
import json
from flask import Blueprint

#####################################################################
# Blueprint for Flask
mid = Blueprint('mid', __name__, url_prefix='/mid')

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

games = []
week_to_check = 1

#####################################################################

def determine_winner_and_update_record(game, string):
    home = game['home']
    away = game['visitor']
    home_team_abbr = common.mapping.get(home)
    away_team_abbr = common.mapping.get(away)

    home_points = 0
    away_points = 0

    home_team = home_team_abbr
    if home_team_abbr in common.nflgamemappingReverse:
        home_team = common.nflgamemappingReverse.get(home_team)

    away_team = away_team_abbr
    if away_team_abbr in common.nflgamemappingReverse:
        away_team = common.nflgamemappingReverse.get(away_team)

    i = 1
    weekstoget = []
    while i < week_to_check:
        weekstoget.append(i)
        i += 1
    home_games_list = []
    away_games_list = []
    if len(weekstoget) > 0:
        home_games_list = nflgame.games(2015, weekstoget, home_team, home_team, 'REG')
        away_games_list = nflgame.games(2015, weekstoget, away_team, away_team, 'REG')
    else:
        home_games_list = nflgame.games(2014, [15, 16, 17], home_team, home_team, 'REG')
        away_games_list = nflgame.games(2014, [15, 16, 17], away_team, away_team, 'REG')

    home_stats = nflgame.combine_game_stats(home_games_list)
    away_stats = nflgame.combine_game_stats(away_games_list)

    home_games = records[home_team_abbr]['win'] + records[home_team_abbr]['loss']
    away_games = records[away_team_abbr]['win'] + records[away_team_abbr]['loss']

    home_games = home_games if home_games is not 0 else 3
    away_games = away_games if away_games is not 0 else 3

    home_rushing = 0
    away_rushing = 0

    home_passing = 0
    away_passing = 0

    home_turnovers = 0
    away_turnovers = 0

    home_td = 0
    away_td = 0

    for p in home_stats:
        if p.team == home_team:
            home_passing += p.passing_yds
            home_rushing += p.rushing_yds
            home_turnovers += p.passing_ints
            home_turnovers += p.fumbles_lost
            home_td += p.passing_tds
            home_td += p.rushing_tds

    for p in away_stats:
        if p.team == away_team:
            away_passing += p.passing_yds
            away_rushing += p.rushing_yds
            away_turnovers += p.passing_ints
            away_turnovers += p.fumbles_lost
            away_td += p.passing_tds
            away_td += p.rushing_tds

    home_turnovers = home_turnovers/home_games
    away_turnovers = away_turnovers/away_games
    if away_turnovers < home_turnovers:
        away_points += 7
    else:
        home_points += 7

    home_passing = home_passing/home_games
    away_passing = away_passing/away_games
    if away_passing > home_passing:
        away_points += 10
    else:
        home_points += 10

    home_rushing = home_rushing/home_games
    away_rushing = away_rushing/away_games
    if away_rushing > home_rushing:
        away_points += 5
    else:
        home_points += 5

    home_td = home_td/home_games
    away_td = away_td/away_games
    if away_td > home_td:
        away_points += 12
    else:
        home_points += 12

    if away_points > home_points:
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
    global schedule, records, games, division_standings
    schedule = common.schedule

    games = common.get_games(uptoweek)

    records = common.update_records(games, records, uptoweek)

    i = uptoweek
    while i <= endweek:
        week = "WEEK {0}".format(i)
        gamestoplay = schedule.get(week)
        string = determine_winners(week, gamestoplay, string)
        string = common.add_breaks_to_string(string)
        division_standings = common.update_division_records(records)
        string = common.print_records_by_div(string, division_standings)
        i += 1
    return string


#####################################################################
# API Endpoints


@mid.route('/guessWeek/<week_to_predict>', methods=['GET'])
def guess_week(week_to_predict):
    global week_to_check, records, division_standings
    records = common.reset_records(records)
    week_to_predict = int(week_to_predict)
    week_to_check = week_to_predict
    string = predict_games(week_to_predict, week_to_predict, common.set_up_html_string())
    return json.dumps({'data': common.finish_html_string(string)}, 200, {'ContentType': 'application/json'})


@mid.route('/guessFromWeek/<week_to_predict>', methods=['GET'])
def guess_from_week(week_to_predict):
    global week_to_check, records, division_standings
    records = common.reset_records(records)
    week_to_predict = int(week_to_predict)
    week_to_check = week_to_predict
    string = predict_games(week_to_predict, 17, common.set_up_html_string())
    return common.finish_html_string(string)
