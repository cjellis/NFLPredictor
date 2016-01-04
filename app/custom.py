from __future__ import division
import nflgame
import common
import json
from flask import Blueprint

#####################################################################
# Blueprint for Flask
custom = Blueprint('custom', __name__, url_prefix='/custom')


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

patriots = {
    #passing
    'passing_att': 0,
    'passing_yds': 5,
    'passing_cmp': 0,
    'passing_ints': 6,
    'passing_tds': 10,

    #rushng
    'rushing_tds': 10,
    'rushing_yds': 5,
    'rushing_att': 0,

    #offensive turnovers
    'fumbles_tot': 1,
    'fumbles_lost': 7,

    #punt returns
    'puntret_tds': 10,
    'puntret_avg': 5,

    #kicking
    'kicking_xptot': 1,
    'kicking_xpmade': 5,
    'kicking_fga': 2,
    'kicking_fgm': 5,

    #defense
    'defense_ffum': 8,
    'defense_int': 8,
    'defense_sk': 5
}

packers = {
    #passing
    'passing_att' : 4,
    'passing_yds' : 15,
    'passing_cmp' : 0,
    'passing_ints' : 6,
    'passing_tds' : 18,

    #rushng
    'rushing_tds' : 17,
    'rushing_yds' : 14,
    'rushing_att' : 10,

    #offensive turnovers
    'fumbles_tot' : 12,
    'fumbles_lost' : 15,

    #punt returns
    'puntret_tds' : 6,
    'puntret_avg' : 5,

    #kicking
    'kicking_xptot' : 17,
    'kicking_xpmade' : 18,
    'kicking_fga' : 16,
    'kicking_fgm' : 18,

    #defense
    'defense_ffum' : 13,
    'defense_int' : 16,
    'defense_sk' : 0
}

panthers = {
    #passing
    'passing_att': 0,
    'passing_yds': 7,
    'passing_cmp': 0,
    'passing_ints': 5,
    'passing_tds': 11,

    #rushng
    'rushing_tds': 12,
    'rushing_yds': 7,
    'rushing_att': 0,

    #offensive turnovers
    'fumbles_tot': 3,
    'fumbles_lost': 9,

    #punt returns
    'puntret_tds': 13,
    'puntret_avg': 3,

    #kicking
    'kicking_xptot': 0,
    'kicking_xpmade': 4,
    'kicking_fga': 1,
    'kicking_fgm': 4,

    #defense
    'defense_ffum': 7,
    'defense_int': 6,
    'defense_sk': 4
}

eagles = {
    #passing
    'passing_att': 5,
    'passing_yds': 8,
    'passing_cmp': 10,
    'passing_ints': 12,
    'passing_tds': 15,

    #rushng
    'rushing_tds': 12,
    'rushing_yds': 6,
    'rushing_att': 3,

    #offensive turnovers
    'fumbles_tot': 10,
    'fumbles_lost': 12,

    #punt returns
    'puntret_tds': 10,
    'puntret_avg': 4,

    #kicking
    'kicking_xptot': 5,
    'kicking_xpmade': 7,
    'kicking_fga': 1,
    'kicking_fgm': 4,

    #defense
    'defense_ffum': 6,
    'defense_int': 6,
    'defense_sk': 5
}

division_standings = []
playoffs = []

games = []
week_to_check = 1

#####################################################################
# Helper Functions


def determine_winner_and_update_record(game, string, stats):
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

    home_stats_totals = {
        'passing_att' : 0,
        'passing_yds' : 0,
        'passing_cmp' : 0,
        'passing_ints' : 0,
        'passing_tds' : 0,

        'rushing_tds' : 0,
        'rushing_yds' : 0,
        'rushing_att' : 0,

        'fumbles_tot' : 0,
        'fumbles_lost' : 0,

        'puntret_tds' : 0,
        'puntret_avg' : 0,

        'kicking_xptot' : 0,
        'kicking_xpmade' : 0,
        'kicking_fga' : 0,
        'kicking_fgm' : 0,

        'defense_ffum' : 0,
        'defense_int': 0,
        'defense_sk' : 0
    }

    away_stats_totals = {
        'passing_att': 0,
        'passing_yds': 0,
        'passing_cmp': 0,
        'passing_ints': 0,
        'passing_tds': 0,

        'rushing_tds': 0,
        'rushing_yds': 0,
        'rushing_att': 0,

        'fumbles_tot': 0,
        'fumbles_lost': 0,

        'puntret_tds': 0,
        'puntret_avg': 0,

        'kicking_xptot': 0,
        'kicking_xpmade': 0,
        'kicking_fga': 0,
        'kicking_fgm': 0,

        'defense_ffum': 0,
        'defense_int': 0,
        'defense_sk': 0
    }

    for p in home_stats:
        if p.team == home_team:
            home_stats_totals['passing_att'] += p.passing_att
            home_stats_totals['passing_yds'] += p.passing_yds
            home_stats_totals['passing_cmp'] += p.passing_cmp
            home_stats_totals['passing_ints'] += p.passing_ints
            home_stats_totals['passing_tds'] += p.passing_tds

            home_stats_totals['rushing_tds'] += p.rushing_tds
            home_stats_totals['rushing_yds'] += p.rushing_yds
            home_stats_totals['rushing_att'] += p.rushing_att

            home_stats_totals['fumbles_tot'] += p.fumbles_tot
            home_stats_totals['fumbles_lost'] += p.fumbles_lost

            home_stats_totals['puntret_tds'] += p.puntret_tds
            home_stats_totals['puntret_avg'] += p.puntret_avg

            home_stats_totals['kicking_xptot'] += p.kicking_xptot
            home_stats_totals['kicking_xpmade'] += p.kicking_xpmade
            home_stats_totals['kicking_fga'] += p.kicking_fga
            home_stats_totals['kicking_fgm'] += p.kicking_fgm

            home_stats_totals['defense_ffum'] += p.defense_ffum
            home_stats_totals['defense_int'] += p.defense_int
            home_stats_totals['defense_sk'] += p.defense_sk

    for p in away_stats:
        if p.team == away_team:
            away_stats_totals['passing_att'] += p.passing_att
            away_stats_totals['passing_yds'] += p.passing_yds
            away_stats_totals['passing_cmp'] += p.passing_cmp
            away_stats_totals['passing_ints'] += p.passing_ints
            away_stats_totals['passing_tds'] += p.passing_tds

            away_stats_totals['rushing_tds'] += p.rushing_tds
            away_stats_totals['rushing_yds'] += p.rushing_yds
            away_stats_totals['rushing_att'] += p.rushing_att

            away_stats_totals['fumbles_tot'] += p.fumbles_tot
            away_stats_totals['fumbles_lost'] += p.fumbles_lost

            away_stats_totals['puntret_tds'] += p.puntret_tds
            away_stats_totals['puntret_avg'] += p.puntret_avg

            away_stats_totals['kicking_xptot'] += p.kicking_xptot
            away_stats_totals['kicking_xpmade'] += p.kicking_xpmade
            away_stats_totals['kicking_fga'] += p.kicking_fga
            away_stats_totals['kicking_fgm'] += p.kicking_fgm

            away_stats_totals['defense_ffum'] += p.defense_ffum
            away_stats_totals['defense_int'] += p.defense_int
            away_stats_totals['defense_sk'] += p.defense_sk

    for stat, value in stats.iteritems():
        total = home_stats_totals.get(stat) + away_stats_totals.get(stat)
        home_percent = 0
        away_percent = 0
        if total is not 0:
            home_percent = home_stats_totals.get(stat) / total
            away_percent = away_stats_totals.get(stat) / total
        home_points += home_percent * value
        away_points += away_percent * value

    if away_points > home_points:
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div>".format(away, home, away)
        records[home_team_abbr]['loss'] += 1
        records[away_team_abbr]['win'] += 1
    else:
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div>".format(away, home, home)
        records[away_team_abbr]['loss'] += 1
        records[home_team_abbr]['win'] += 1
    return string


def determine_winners(week_number, games, string, stats):
    string += "<div><h3>{0}</h3></div>".format(week_number)
    string += "<table>"
    i = 0
    for game in games:
        if i == 0:
            string += "<tr><td>"
        if i == 1:
            string += "</td><td>"
        string = determine_winner_and_update_record(game, string, stats)
        i += 1
        if i == 2:
            string += "</td></tr>"
            i = 0
    string += "</table>"
    return string


def predict_games(uptoweek, endweek, string, stats):
    global schedule, records, games, division_standings
    schedule = common.schedule

    games = common.get_games(uptoweek)

    records = common.update_records(games, records, uptoweek)

    i = uptoweek
    while i <= endweek:
        week = "WEEK {0}".format(i)
        gamestoplay = schedule.get(week)
        string = determine_winners(week, gamestoplay, string, stats)
        string = common.add_breaks_to_string(string)
        division_standings = common.update_division_records(records)
        string = common.print_records_by_div(string, division_standings)
        i += 1
    return string

#####################################################################
# API Endpoints


@custom.route('/patriots/guessWeek/<week_to_predict>', methods=['GET'])
def guess_week_patriots(week_to_predict):
    global week_to_check, records, division_standings
    records = common.reset_records(records)
    week_to_predict = int(week_to_predict)
    week_to_check = week_to_predict
    stats = patriots
    string = predict_games(week_to_predict, week_to_predict, common.set_up_html_string(), stats)
    return json.dumps({'data': common.finish_html_string(string)}, 200, {'ContentType': 'application/json'})


@custom.route('/packers/guessWeek/<week_to_predict>', methods=['GET'])
def guess_week_packers(week_to_predict):
    global week_to_check, records, division_standings
    records = common.reset_records(records)
    week_to_predict = int(week_to_predict)
    week_to_check = week_to_predict
    stats = packers
    string = predict_games(week_to_predict, week_to_predict, common.set_up_html_string(), stats)
    return json.dumps({'data': common.finish_html_string(string)}, 200, {'ContentType': 'application/json'})


@custom.route('/panthers/guessWeek/<week_to_predict>', methods=['GET'])
def guess_week_panthers(week_to_predict):
    global week_to_check, records, division_standings
    records = common.reset_records(records)
    week_to_predict = int(week_to_predict)
    week_to_check = week_to_predict
    stats = panthers
    string = predict_games(week_to_predict, week_to_predict, common.set_up_html_string(), stats)
    return json.dumps({'data': common.finish_html_string(string)}, 200, {'ContentType': 'application/json'})


@custom.route('/eagles/guessWeek/<week_to_predict>', methods=['GET'])
def guess_week_eagles(week_to_predict):
    global week_to_check, records, division_standings
    records = common.reset_records(records)
    week_to_predict = int(week_to_predict)
    week_to_check = week_to_predict
    stats = eagles
    string = predict_games(week_to_predict, week_to_predict, common.set_up_html_string(), stats)
    return json.dumps({'data': common.finish_html_string(string)}, 200, {'ContentType': 'application/json'})

