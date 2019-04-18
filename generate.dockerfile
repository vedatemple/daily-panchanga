FROM python:3.7

WORKDIR /src

RUN pip install git+https://github.com/astrorigin/pyswisseph@master -U
RUN pip install git+https://github.com/sanskrit-coders/jyotisha@master -U

COPY Dockerfile /src

ENTRYPOINT ["bash"]