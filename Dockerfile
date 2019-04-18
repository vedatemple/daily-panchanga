FROM python:3.7.3-alpine

RUN pip install cherrypy

WORKDIR /app
COPY seattle_2019.json /app
COPY serve_data.py /app


EXPOSE 5000
ENTRYPOINT [ "python", "serve_data.py" ]