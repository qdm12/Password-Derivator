FROM ubuntu
RUN apt-get update && apt-get install -y python python-pip
RUN mkdir -p /derivatex
WORKDIR /derivatex
COPY install.py main.py ./
RUN python install.py terminal
COPY derivatex ./
COPY dockerscript.sh ./
RUN chmod +x /derivatex/dockerscript.sh
CMD './derivatex/dockerscript.sh'