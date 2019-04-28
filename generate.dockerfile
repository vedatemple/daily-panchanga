FROM python:3.7
WORKDIR /src

RUN apt-get update && apt-get -y install less 
RUN pip install --upgrade pip
RUN pip install git+https://github.com/vedatemple/pyswisseph@master -U
RUN pip install git+https://github.com/vedatemple/jyotisha@master -U
RUN pip install ics

ENTRYPOINT ["bash"]