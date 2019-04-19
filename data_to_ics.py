from ics import Calendar, Event
from datetime import datetime
from sys import stdin
import json

json_input = stdin.read()
data = json.loads(json_input)

    # "2019-1-1": {
    #     "date": "2019-1-1",
    #     "month": "January",
    #     "weekday": "Tue",
    #     "sunrise": "08:03",
    #     "sunset": "16:22",
    #     "rahu_start": "14:17",
    #     "rahu_end": "15:20",
    #     "yama_start": "10:08",
    #     "yama_end": "11:10",
    #     "tithi": [
    #         {
    #             "name": "Kṛṣṇa-Ekādaśī",
    #             "end": "11:58"
    #         }
    #     ],
    #     "nakshatram": [
    #         {
    #             "name": "Viśākhā",
    #             "end": "20:09"
    #         }
    #     ],
    #     "yogam": [
    #         {
    #             "name": "Dhṛtiḥ",
    #             "end": "13:11"
    #         }
    #     ],
    #     "karanam": [
    #         {
    #             "name": "Bālavam",
    #             "end": "11:58"
    #         },
    #         {
    #             "name": "Kaulavam",
    #             "end": "00:16(+1)"
    #         }
    #     ]
    # },


def anga_to_string(item, anga):
    
    description_array = []

    for v in item[anga]:
        description = f"{anga}: {v['name']}"
        if 'end' in v:
            description = description + f" until {v['end']}"
        description_array.append(description)

    return '\n'.join(description_array)

def item_to_string(item):
    description = f"""{i['weekday']} {i['date']} 
Daytime: {i['sunrise']} to {i['sunset']}

Month: {i['lunar_month']}
{anga_to_string(i, 'tithi')}
{anga_to_string(i, 'nakshatram')}
{anga_to_string(i, 'yogam')}
{anga_to_string(i, 'karanam')}

Rahu kala: {i['rahu_start']} to {i['rahu_end']}
Yama kala: {i['yama_start']} to {i['yama_end']}"""

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
    
    ical_event = Event()
    ical_event.name = item_to_name(item)
    ical_event.begin = datetime.strptime(item['date'], '%Y-%m-%d')
    ical_event.end = datetime.strptime(item['date'], '%Y-%m-%d')
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

