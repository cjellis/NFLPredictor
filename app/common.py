import nflgame
import readfromcsv

#####################################################################
# Global Variables
week_to_record_cache = {}

week_to_games_cache = {}

current_records = {
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

algorithms = ['basic', 'mid', 'packers', 'patriots', 'panthers']

algo_records = {
    'basic': {'right': 84, 'wrong': 48},
    'mid': {'right': 76, 'wrong': 56},
    'packers': {'right': 0, 'wrong': 0},
    'patriots': {'right': 0, 'wrong': 0},
    'panthers': {'right': 0, 'wrong': 0}
}

mapping = {
    'Colts': 'IND',
    'Texans': 'HOU',
    'Seahawks': 'SEA',
    'Bengals': 'CIN',
    'Bills': 'BUF',
    'Titans': 'TEN',
    'Bears': 'CHI',
    'Chiefs': 'KCC',
    'Saints': 'NOS',
    'Eagles': 'PHI',
    'Rams': 'STL',
    'Packers': 'GBP',
    'Jaguars': 'JAC',
    'Buccaneers': 'TBB',
    'Redskins': 'WAS',
    'Falcons': 'ATL',
    'Browns': 'CLE',
    'Ravens': 'BAL',
    'Cardinals': 'ARI',
    'Lions': 'DET',
    'Broncos': 'DEN',
    'Raiders': 'OAK',
    'Patriots': 'NEP',
    'Cowboys': 'DAL',
    '49ers': 'SFO',
    'Giants': 'NYG',
    'Steelers': 'PIT',
    'Chargers': 'SDG',
    'Jets': 'NYJ',
    'Dolphins': 'MIA',
    'Vikings': 'MIN',
    'Panthers': 'CAR'
}

nflgamemapping = {
    'NE': 'NEP',
    'GB': 'GBP',
    'KC': 'KCC',
    'NO': 'NOS',
    'SD': 'SDG',
    'TB': 'TBB',
    'SF': 'SFO'
}

nflgamemappingReverse = {
    'NEP': 'NE',
    'GBP': 'GB',
    'KCC': 'KC',
    'NOS': 'NO',
    'SDG': 'SD',
    'TBB': 'TB',
    'SFO': 'SF'
}

divisions = {'AFCE': ['NEP', 'BUF', 'NYJ', 'MIA'],
             'AFCN': ['CIN', 'PIT', 'BAL', 'CLE'],
             'AFCS': ['IND', 'TEN', 'HOU', 'JAC'],
             'AFCW': ['DEN', 'OAK', 'SDG', 'KCC'],
             'NFCE': ['DAL', 'NYG', 'WAS', 'PHI'],
             'NFCN': ['GBP', 'MIN', 'CHI', 'DET'],
             'NFCS': ['CAR', 'ATL', 'TBB', 'NOS'],
             'NFCW': ['ARI', 'STL', 'SEA', 'SFO'],
             }

#####################################################################
# Helper Functions

def set_up_html_string():
    return ""#"<html><style>div {font-size:10;}</style><body>"


def finish_html_string(string):
    #string += "</body></html>"
    return string


def get_games(uptoweek):
    if uptoweek in week_to_games_cache.keys():
        return week_to_games_cache.get(uptoweek)
    weekstoget = []
    i = 1
    while i < uptoweek:
        weekstoget.append(i)
        i += 1
    games = []
    if len(weekstoget) > 0:
        games = nflgame.games(2015, weekstoget)
    week_to_games_cache[uptoweek] = games
    return games


def update_records(games, records, uptoweek):
    # if uptoweek in week_to_record_cache.keys():
        # print "Cache hit"
        # return week_to_record_cache.get(uptoweek)
    for game in games:
        winner = game.winner
        loser = game.loser
        if winner in nflgamemapping:
            winner = nflgamemapping.get(winner)
        if loser in nflgamemapping:
            loser = nflgamemapping.get(loser)
        records[loser]['loss'] += 1
        records[winner]['win'] += 1
    week_to_record_cache[uptoweek] = records
    return records


def add_breaks_to_string(string):
    string += "<br><br>"
    return string


def update_division_records(records):
    division_standings = []
    for div, teams in divisions.iteritems():
        team_records = []
        for team in teams:
            rec = records.get(team)
            team_records.append({'name': team, 'record': rec})
        team_records = sorted(team_records, key=lambda a: a['record']['loss'])
        division_standings.append({'division': div, 'records': team_records})
    return sorted(division_standings, key=lambda a: a['division'])


def print_records_by_div(string, division_standings):
    string += "<table>"
    i = 0
    for div in division_standings:
        if i == 0:
            string += "<tr><td>"
        if i == 1:
            string += "</td><td>"
        string += "<div><h3>{0}</h3></div>".format(div['division'])
        for team in div['records']:
            string += "<div>{0} W:{1} L:{2}</div>".format(team['name'], team['record']['win'], team['record']['loss'])
        i += 1
        if i == 2:
            string += "</td></tr>"
            i = 0
    return string


def reset_records(records):
    for key, value in records.iteritems():
        records[key]['win'] = 0
        records[key]['loss'] = 0
    return records

#####################################################################
# Get the schedule on initialization
schedule = readfromcsv.get_schedule()
