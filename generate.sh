#!/bin/bash

./generate_json.py --year $1 > data/veda_seattle_$1.json
cat data/veda_seattle_$1.json | ./json_to_ical.py > data/veda_seattle_$1.ics
