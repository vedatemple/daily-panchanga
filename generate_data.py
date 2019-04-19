
# Based off https://github.com/sanskrit-coders/jyotisha/blob/master/jyotisha/panchangam/scripts/write_monthly_panchangam_tex.py

from datetime import datetime
from pytz import timezone as tz
import swisseph as swe

import json
import jyotisha
import jyotisha.panchangam.spatio_temporal.annual
from jyotisha.panchangam.spatio_temporal import City

MON = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
        10: 'October', 11: 'November', 12: 'December'}
WDAY = {0: 'Sun', 1: 'Mon', 2: 'Tue',
        3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}

seattle = City("Seattle", "47.6062", "-122.3321", "America/Los_Angeles")
year = 2019

panchangam = jyotisha.panchangam.spatio_temporal.annual.get_panchangam(city=seattle, year=year, script="iast")

samvatsara_id = (panchangam.year - 1568) % 60 + 1  # distance from prabhava
samvatsara_names = '%s–%s' % (jyotisha.panchangam.temporal.NAMES['SAMVATSARA_NAMES'][panchangam.script][samvatsara_id],
                                jyotisha.panchangam.temporal.NAMES['SAMVATSARA_NAMES'][panchangam.script][(samvatsara_id % 60) + 1])

panchangam.get_kaalas()

# print (str(panchangam))

# {
#     'data': 'tithi_data',               # panchangam.tithi_data[d]
#     'names': 'TITHI_NAMES',             # jyotisha.panchangam.temporal.NAMES['TITHI_NAMES']
#     'id': 'tithi_ID',                   # tithi_ID, tithi_end_jd in panchangam.tithi_data[d]
#     'end_jd': 'tithi_end_jd',           # tithi_ID, tithi_end_jd in panchangam.tithi_data[d]
#     'json_name': 'tithi'
# },

entities = []

for e_base in ['tithi', 'nakshatram', 'yogam', 'karanam']:
    entities.append(
        {
            'data': '%s_data' % e_base,
            'names': '%s_NAMES' % e_base.upper(),
            'id': '%s_ID' % e_base,
            'end_jd': '%s_end_jd' % e_base,
            'json_name': e_base
        }
    )

output_collector = {}

def enumerate_anga(panchangam, anga_entity, d):
    anga_collector = []

    data = getattr(panchangam, anga_entity['data'])
    if data[d]:
        for id, end_jd in data[d]:
            anga_name = jyotisha.panchangam.temporal.NAMES[anga_entity['names']][panchangam.script][id]
            if end_jd is None:
                anga_collector.append({'name': anga_name})
                # print ("    %s" % (anga_name))
            else:
                anga_end = jyotisha.panchangam.temporal.Time(24 * (end_jd - jd)).toString(format=panchangam.fmt)
                anga_collector.append({'name': anga_name, 'end': anga_end})
                # print ("    %s: %s" % (anga_name, anga_end))

    return anga_collector

for d in range(1, jyotisha.panchangam.temporal.MAX_SZ - 1):
    try:
        [y, m, dt, t] = swe.revjul(panchangam.jd_start_utc + d - 1)
        local_time = tz(panchangam.city.timezone).localize(datetime(y, m, dt, 6, 0, 0))
        tz_off = (datetime.utcoffset(local_time).days * 86400 +
                datetime.utcoffset(local_time).seconds) / 3600.0
        jd = panchangam.jd_start_utc - tz_off / 24.0 + d - 1
        sunrise = jyotisha.panchangam.temporal.Time(24 * (panchangam.jd_sunrise[d] - jd)).toString(format=panchangam.fmt)
        sunset = jyotisha.panchangam.temporal.Time(24 * (panchangam.jd_sunset[d] - jd)).toString(format=panchangam.fmt)
        rahu_start = jyotisha.panchangam.temporal.Time(24 * (panchangam.kaalas[d]['rahu'][0] - jd)).toString(format=panchangam.fmt)
        rahu_end = jyotisha.panchangam.temporal.Time(24 * (panchangam.kaalas[d]['rahu'][1] - jd)).toString(format=panchangam.fmt)
        yama_start = jyotisha.panchangam.temporal.Time(24 * (panchangam.kaalas[d]['yama'][0] - jd)).toString(format=panchangam.fmt)
        yama_end = jyotisha.panchangam.temporal.Time(24 * (panchangam.kaalas[d]['yama'][1] - jd)).toString(format=panchangam.fmt)        
        lunar_month = jyotisha.panchangam.temporal.get_chandra_masa(panchangam.lunar_month[d],
                                                                 jyotisha.panchangam.temporal.NAMES, panchangam.script)

        d_str = '%s-%s-%s' % (year, m, dt)
        output_collector[d_str] = {
            'date': d_str,
            'month': MON[m],
            'weekday': WDAY[panchangam.weekday[d]],
            'sunrise': sunrise,
            'sunset': sunset,
            'rahu_start': rahu_start,
            'rahu_end': rahu_end,
            'yama_start': yama_start,
            'yama_end': yama_end,
            'lunar_month': lunar_month

        }
    except:
        pass

    for e in entities:
        output_collector[d_str][e['json_name']] = enumerate_anga(panchangam, e, d)


json_output = json.dumps(output_collector, indent=4, ensure_ascii=False)
print (json_output)

# data = json.loads(json_output)
# data_day = data['2019-4-4']
# print (json.dumps(data_day, indent=4, ensure_ascii=False))