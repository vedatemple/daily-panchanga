#!/bin/bash

./generate_json.py --city $1 --year $2  > data/veda_$1_$2.json
cat data/veda_$1_$2.json | ./json_to_ical.py --city $1 > data/veda_$1_$2.ics
