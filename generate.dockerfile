FROM python:3.7

WORKDIR /src

RUN pip install git+https://github.com/astrorigin/pyswisseph@master -U
RUN pip install git+https://github.com/sanskrit-coders/jyotisha@master -U
RUN pip install ics
RUN apt-get update && apt-get -y install less 

COPY Dockerfile /src

ENTRYPOINT ["bash"]