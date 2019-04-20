FROM python:3.7.3-alpine

RUN pip install cherrypy

WORKDIR /app
COPY data/veda_seattle_2019.json /app/seattle_2019.json
COPY serve_data.py /app


EXPOSE 5000
ENTRYPOINT [ "python", "serve_data.py" ]