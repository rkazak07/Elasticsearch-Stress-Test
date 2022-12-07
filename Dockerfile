FROM ubuntu:22.04


MAINTAINER Ramazan KAZAK (ramazankazak_2016@hotmail.com)


WORKDIR /app


RUN apt-get update && apt-get install -y \
    python3-pip


RUN pip3 install --upgrade pip



COPY . /app



RUN pip install -r requirements.txt



ENTRYPOINT ["python3", "es-perf-test.py"]
