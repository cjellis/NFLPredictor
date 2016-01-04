from __future__ import division
import common
from flask import Blueprint

fullSeason = Blueprint('fullSeason', __name__, url_prefix='/fullSeason')

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
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div><br>".format(away, home, away)
        records[home_team_abbr]['loss'] += 1
        records[away_team_abbr]['win'] += 1
    else:
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div><br>".format(away, home, home)
        records[away_team_abbr]['loss'] += 1
        records[home_team_abbr]['win'] += 1
    return string


def return_winner(game, string):
    ret = []
    home = game['home']
    away = game['visitor']
    home_team_record = records.get(home)
    away_team_record = records.get(away)
    away_percent = 1 if away_team_record['loss'] is 0 else away_team_record['win']/away_team_record['loss']
    home_percent = 1 if home_team_record['loss'] is 0 else home_team_record['win']/home_team_record['loss']
    if away_percent > home_percent:
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div><br>".format(away, home, away)
        ret.append(away)
    else:
        string += "<div>{0} @ {1}</div> <div> Winner: {2}</div><br>".format(away, home, home)
        ret.append(home)
    ret.append(string)
    return ret


def determine_winners(week_number, games, string):
    string += "{0}".format(week_number)
    for game in games:
        string = determine_winner_and_update_record(game, string)
    return string


def determine_playoff_matchups(string):
    afc = []
    afc_5th = {'name': 'holder', 'record': {'win': 0, 'loss': 0}}
    afc_6th = {'name': 'holder', 'record': {'win': 0, 'loss': 0}}
    nfc = []
    nfc_5th = {'name': 'holder', 'record': {'win': 0, 'loss': 0}}
    nfc_6th = {'name': 'holder', 'record': {'win': 0, 'loss': 0}}
    for div in division_standings:
        if div['division'][0:1] is 'A':
            afc.append(div['records'][0])
            if div['records'][1]['record']['win'] > afc_5th['record']['win']:
                afc_5th = div['records'][1]
                if div['records'][2]['record']['win'] > afc_6th['record']['win']:
                    afc_6th = div['records'][2]
            else:
                if div['records'][1]['record']['win'] > afc_6th['record']['win']:
                    afc_6th = div['records'][1]
        else:
            nfc.append(div['records'][0])
            if div['records'][1]['record']['win'] > nfc_5th['record']['win']:
                nfc_5th = div['records'][1]
                if div['records'][2]['record']['win'] > nfc_6th['record']['win']:
                    nfc_6th = div['records'][2]
            else:
                if div['records'][1]['record']['win'] > nfc_6th['record']['win']:
                    nfc_6th = div['records'][1]
    afc = sorted(afc, key=lambda a: a['record']['loss'])
    nfc = sorted(nfc, key=lambda a: a['record']['loss'])

    string = common.add_breaks_to_string(string)
    string += "<div>Playoff Week 1</div>"
    game1 = {'home': afc[2]['name'], 'visitor': afc_6th['name']}
    game2 = {'home': afc[3]['name'], 'visitor': afc_5th['name']}
    game3 = {'home': nfc[2]['name'], 'visitor': afc_6th['name']}
    game4 = {'home': nfc[3]['name'], 'visitor': afc_5th['name']}

    winner1 = return_winner(game1, string)
    string += winner1[1]
    winner2 = return_winner(game2, string)
    string += winner2[1]
    winner3 = return_winner(game3, string)
    string += winner3[1]
    winner4 = return_winner(game4, string)
    string += winner4[1]

    string = common.add_breaks_to_string(string)
    string += "<div>Playoff Week 2</div>"
    game1 = {'home': afc[0]['name'], 'visitor': winner1[0]}
    game2 = {'home': afc[1]['name'], 'visitor': winner2[0]}
    game3 = {'home': nfc[0]['name'], 'visitor': winner3[0]}
    game4 = {'home': nfc[1]['name'], 'visitor': winner4[0]}

    winner1 = return_winner(game1, string)
    string += winner1[1]
    winner2 = return_winner(game2, string)
    string += winner2[1]
    winner3 = return_winner(game3, string)
    string += winner3[1]
    winner4 = return_winner(game4, string)
    string += winner4[1]

    string = common.add_breaks_to_string(string)
    string += "<div>Championships</div>"
    game1 = {'home': winner1[0], 'visitor': winner2[0]}
    game2 = {'home': winner3[0], 'visitor': winner4[0]}

    winner1 = return_winner(game1, string)
    string += winner1[1]
    winner2 = return_winner(game2, string)
    string += winner2[1]

    string = common.add_breaks_to_string(string)
    string += "<div>Superbowl</div>"
    game1 = {'home': winner1[0], 'visitor': winner2[0]}
    winner1 = return_winner(game1, string)
    string += winner1[1]

    string += "<div>Champion: {0}</div>".format(winner1[0])
    return string


def run_each_week(string):
    global division_standings
    for week, games in sorted(schedule.iteritems(),  key=lambda (k, v): int(k.split(" ")[1])):
        string = determine_winners(week, games, string)
        string = common.add_breaks_to_string(string)
        division_standings = common.update_division_records(records)
        string = common.print_records_by_div(string, division_standings)
        string = common.add_breaks_to_string(string)
    return string


#@fullSeason.route('/findChampion', methods=['GET'])
def find_champion():
    global schedule, records
    records = common.reset_records(records)
    string = common.set_up_html_string()
    schedule = common.schedule
    string = run_each_week(string)
    string = determine_playoff_matchups(string)
    return common.finish_html_string(string)

