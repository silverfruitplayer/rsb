FROM python:3.9.6
RUN apt update && apt upgrade -y
RUN cd /
RUN git clone https://github.com/silverfruitplayer/rsb
RUN cd rsb
WORKDIR /rsb
RUN pip3 install -r requirements.txt
CMD python3 rsb.py
