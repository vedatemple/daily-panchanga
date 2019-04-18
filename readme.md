# daily-panchanga

# generate data (seattle)

`docker build -f generate.dockerfile -t daily-panchanga .`

`docker run -it -v $(PWD):/host daily-panchanga`

`cd /host && python generate_data.py`

# serve data (seattle)

`docker build -f Dockerfile -t serve-daily-panchanga .`

`docker run -p 5000:5000 serve-daily-panchanga`

`curl http://localhost:5000`

`curl http://localhost:5000?date=2019-1-1`
