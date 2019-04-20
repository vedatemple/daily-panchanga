#!/usr/local/bin/python
# Based off https://github.com/sanskrit-coders/jyotisha/blob/master/jyotisha/panchangam/scripts/write_monthly_panchangam_tex.py

from datetime import datetime
from pytz import timezone as tz
import swisseph as swe
import argparse

import json
import jyotisha
from jyotisha.panchangam import temporal
import jyotisha.panchangam.spatio_temporal.annual
from jyotisha.panchangam.spatio_temporal import City
from indic_transliteration import xsanscript as sanscript

MON = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September',
        10: 'October', 11: 'November', 12: 'December'}
WDAY = {0: 'sunday', 1: 'monday', 2: 'tuesday',
        3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday'}

seattle = City("Seattle", "47.6062", "-122.3321", "US/Pacific")

parser = argparse.ArgumentParser(description='Generate panchanga data for Seattle')
parser.add_argument('--year', dest='year', type=int, default=2019, help='year (default: 2019)')
args = parser.parse_args()

# based off https://github.com/sanskrit-coders/jyotisha/blob/master/jyotisha/names/init_names_auto.py
def get_names(fname='./names.json'):
  scripts = [sanscript.DEVANAGARI, sanscript.IAST, sanscript.TAMIL, sanscript.TELUGU]
  with open(fname) as f:
    import json
    names_dict = json.load(f)
    for dictionary in names_dict:
      if dictionary != 'VARA_NAMES':
        # Vara Names follow zero indexing, rest don't
        names_dict[dictionary]['hk'].insert(0, 'aspaShTam')

      for scr in scripts:
        names_dict[dictionary][scr] = [sanscript.transliterate(name, 'hk', scr) for name in names_dict[dictionary]['hk']]
    return names_dict


NAMES = get_names()
panchangam = jyotisha.panchangam.spatio_temporal.annual.get_panchangam(city=seattle, year=args.year, script="iast", precomputed_json_dir="./data/jyotisha")

samvatsara_id = (panchangam.year - 1568) % 60 + 1  # distance from prabhava
samvatsara_names = '%s–%s' % (NAMES['SAMVATSARA_NAMES'][panchangam.script][samvatsara_id],
                                NAMES['SAMVATSARA_NAMES'][panchangam.script][(samvatsara_id % 60) + 1])

panchangam.get_kaalas()

# print (str(panchangam))

# {
#     'data': 'tithi_data',               # panchangam.tithi_data[d]
#     'names': 'TITHI_NAMES',             # NAMES['TITHI_NAMES']
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
            anga_name = NAMES[anga_entity['names']][panchangam.script][id]
            if end_jd is None:
                anga_collector.append({'name': anga_name})
                # print ("    %s" % (anga_name))
            else:
                anga_end = temporal.Time(24 * (end_jd - jd)).toString(format=panchangam.fmt)
                anga_collector.append({'name': anga_name, 'end': anga_end})
                # print ("    %s: %s" % (anga_name, anga_end))

    return anga_collector

samvatsara_id = (panchangam.year - 1568) % 60 + 1  # distance from prabhava
samvatsara_names = (NAMES['SAMVATSARA_NAMES'][panchangam.script][samvatsara_id],
                    NAMES['SAMVATSARA_NAMES'][panchangam.script][(samvatsara_id % 60) + 1])
yname = samvatsara_names[0]  # Assign year name until Mesha Sankranti

for d in range(1, temporal.MAX_SZ - 1):
    try:
        [y, m, dt, t] = swe.revjul(panchangam.jd_start_utc + d - 1)
        local_time = tz(panchangam.city.timezone).localize(datetime(y, m, dt, 6, 0, 0))
        tz_off = (datetime.utcoffset(local_time).days * 86400 +
                datetime.utcoffset(local_time).seconds) / 3600.0
        jd = panchangam.jd_start_utc - tz_off / 24.0 + d - 1

        sunrise = temporal.Time(24 * (panchangam.jd_sunrise[d] - jd)).toString(format=panchangam.fmt)
        sunset = temporal.Time(24 * (panchangam.jd_sunset[d] - jd)).toString(format=panchangam.fmt)
        moonrise = temporal.Time(24 * (panchangam.jd_moonrise[d] - jd)).toString(format=panchangam.fmt)
        moonset = temporal.Time(24 * (panchangam.jd_moonset[d] - jd)).toString(format=panchangam.fmt)

        rahu_start = temporal.Time(24 * (panchangam.kaalas[d]['rahu'][0] - jd)).toString(format=panchangam.fmt)
        rahu_end = temporal.Time(24 * (panchangam.kaalas[d]['rahu'][1] - jd)).toString(format=panchangam.fmt)
        yama_start = temporal.Time(24 * (panchangam.kaalas[d]['yama'][0] - jd)).toString(format=panchangam.fmt)
        yama_end = temporal.Time(24 * (panchangam.kaalas[d]['yama'][1] - jd)).toString(format=panchangam.fmt)        
        gulika_start = temporal.Time(24 * (panchangam.kaalas[d]['gulika'][0] - jd)).toString(format=panchangam.fmt)
        gulika_end = temporal.Time(24 * (panchangam.kaalas[d]['gulika'][1] - jd)).toString(format=panchangam.fmt)        

        lunar_month = temporal.get_chandra_masa(panchangam.lunar_month[d],
                                                                 NAMES, panchangam.script)
        solar_month = NAMES['RASHI_NAMES'][panchangam.script][panchangam.solar_month[d]]
        solar_day = panchangam.solar_month_day[d]

        ayana = NAMES['AYANA_NAMES'][panchangam.script][panchangam.solar_month[d]]
        rtu = NAMES['RTU_NAMES'][panchangam.script][panchangam.solar_month[d]]

        if panchangam.solar_month[d] == 1:
            # Flip the year name for the remaining days
            yname = samvatsara_names[1]

        d_str = '%s-%s-%s' % (args.year, '{0:02d}'.format(m), '{0:02d}'.format(dt))

        output_collector[d_str] = {
            'date': d_str,
            'month': MON[m],
            'weekday': WDAY[panchangam.weekday[d]],
            'sunrise': sunrise,
            'sunset': sunset,
            'moonrise': moonrise,
            'moonset': moonset,
            'rahu_start': rahu_start,
            'rahu_end': rahu_end,
            'yama_start': yama_start,
            'yama_end': yama_end,
            'gulika_start': gulika_start,
            'gulika_end': gulika_end,
            'samvatsara': yname,
            'ayana': ayana,
            'rtu': rtu,
            'lunar_month': lunar_month,
            'solar_month': solar_month,
            'solar_day': solar_day
        }
    except:
        pass

    for e in entities:
        output_collector[d_str][e['json_name']] = enumerate_anga(panchangam, e, d)


json_output = json.dumps(output_collector, indent=4, ensure_ascii=False)
print (json_output)
