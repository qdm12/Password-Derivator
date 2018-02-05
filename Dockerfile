FROM python:alpine
RUN apk add --no-cache make gcc g++
RUN pip install -U cffi pip setuptools
RUN mkdir -p /safe
WORKDIR /safe
COPY derivatex /safe
COPY install.py main.py dockerscript.sh /safe/
RUN python install.py terminal
ENTRYPOINT ['/safe/dockerscript.sh']
