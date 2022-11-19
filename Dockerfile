FROM python:3.8-slim-buster

MAINTAINER Ramazan KAZAK


WORKDIR /app


# Edit Elasticsearch Configuration

ENV host=10.10.33.101
ENV user=elastic
ENV pass=elastic
ENV indices=5
ENV documents=2
ENV clients=10
ENV seconds=900
ENV shards=4
ENV replicas=1 
ENV bulk_size=500
ENV max_fields_per_doc=50
ENV max_size_per_field=500
ENV stats_frequency=30



RUN pip install elasticsearch7

COPY . .

CMD python es-perf-test.py  --es_ip $host \
        --indices $indices --documents $documents \
        --client_conn $clients --seconds $seconds \
        --number-of-shards $shards \
        --number-of-replicas $replicas \
        --bulk-size $bulk_size \
        --max-fields-per-document $max_fields_per_doc \
        --max-size-per-field $max_size_per_field \
        --stats-frequency $stats_frequency 
        --user $user \
        --pass $pass \
        --no-verify

