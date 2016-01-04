import csv
import os


#####################################################################
# parses the csv file and creates the schedule for the season
def get_schedule():
    weeks = {}
    with open(os.path.join(os.path.dirname(__file__), 'nfl-2015-schedule.csv'), 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 1
        week = 'WEEK 1'
        currentweek = []
        for row in reader:
            if row['Week'] != week:
                weeks[week] = currentweek
                week = row['Week']
                i += 1
                currentweek = []
            currentweek.append({'visitor': row['Visitor'], 'home': row['Home'][1:]})
    weeks[week] = currentweek
    return weeks
