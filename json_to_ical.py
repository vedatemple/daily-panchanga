#!/usr/local/bin/python

# This file reads stdin for data in the format output by generate_json.py
# and outputs an ical calendar to stdout
#
# See the entries in data/veda_seattle_2019.json for the expected input schema

from ics import Calendar, Event
from datetime import datetime, date, time, timedelta
from sys import stdin
import json, pytz

json_input = stdin.read()
data = json.loads(json_input)

def anga_to_string(item, anga, anga_name):
    description_array = []

    for v in item[anga]:
        description = f"{anga_name}: {v['name']}"
        if 'end' in v:
            description = description + f" until {v['end']}"
        description_array.append(description)

    return '\n'.join(description_array)

def item_to_string(item):
    description = f"""{i['weekday']} {i['date']} 
daytime: {i['sunrise']} to {i['sunset']}

māsa (lunar): {i['lunar_month']}
māsa (solar): {i['solar_month']} - {i['solar_day']}
{anga_to_string(i, 'tithi', 'tithi')}
{anga_to_string(i, 'nakshatram', 'nakṣatra')}
{anga_to_string(i, 'yogam', 'yoga')}
{anga_to_string(i, 'karanam', 'karaṇa')}

varṣa: {i['samvatsara']}
ayana: {i['ayana']}
r̥tu: {i['rtu']}

rāhu kāla: {i['rahu_start']} to {i['rahu_end']}
yama kāla: {i['yama_start']} to {i['yama_end']}
gulika kāla: {i['gulika_start']} to {i['gulika_end']}
moon above horizon: {i['moonrise']} to {i['moonset']}"""

    return description

def item_to_name(item):
    name = ''
    try:
        name = name + item['tithi'][0]['name']
    except:
        pass

    try:
        name = name + ' / ' + item['nakshatram'][0]['name']
    except:
        pass

    return name

def item_to_ical(item):
        
    event_date = datetime.strptime(item['date'], '%Y-%m-%d')
    pacific = pytz.timezone('US/Pacific')
    pacific_date = pacific.localize(datetime(event_date.year, event_date.month, event_date.day, 0, 0, 0))

    ical_event = Event()
    ical_event.name = item_to_name(item)
    ical_event.begin = pacific_date
    ical_event.end = pacific_date  + timedelta(days=1)
    ical_event.uid = 'veda_daily_panchanga_' + item['date']
    ical_event.description = item_to_string(item)
    return ical_event

ical = Calendar()

for d in data.keys():
    i = data[d]

    if not 'sunrise' in i:
        continue

    ical_event = item_to_ical(i)
    ical.events.add(ical_event)

print (ical)

