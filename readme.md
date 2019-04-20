# daily-panchanga

# generate data (seattle)

- build the docker image: `docker build -f generate.dockerfile -t daily-panchanga .`
- run the docker image: `docker run -it -v $(PWD):/host daily-panchanga`
- in the image, generate the data: `cd /host && ./generate.sh 2019`
- the output data will be in `./data/veda_seattle_2019.ics`

Note: on windows use `%PWD%` in place of `$(PWD)` for the volume mount

# serve data (seattle)

- build the image: `docker build -f Dockerfile -t serve-daily-panchanga .`
- run the image locally: `docker run -p 5000:5000 serve-daily-panchanga`
- validate (daily): `curl http://localhost:5000`
- validate (date): `curl http://localhost:5000?date=2019-1-1`
