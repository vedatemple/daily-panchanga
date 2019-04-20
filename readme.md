# daily-panchanga

# generate data (seattle)

- build the docker image: `docker build -f generate.dockerfile -t daily-panchanga .`
- run the docker image: `docker run -it -v $(PWD):/host daily-panchanga`
- in the image, generate the data file and save to a file: `cd /host && python generate_json.py > seattle_2019.json`
- in the image, take the data file and convert it to ical: `cat seattle_2019.json | python json_to_ics.py  > seattle_2019.ics`

# serve data (seattle)

- build the image: `docker build -f Dockerfile -t serve-daily-panchanga .`
- run the image locally: `docker run -p 5000:5000 serve-daily-panchanga`
- validate (daily): `curl http://localhost:5000`
- validate (date): `curl http://localhost:5000?date=2019-1-1`
