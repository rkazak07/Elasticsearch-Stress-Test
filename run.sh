#!/bin/bash

# Linux Unix start
# Change Variables

indices=5
documents=2
clients=10
seconds=900
shards=4
replicas=1
bulk_size=500
max_fields_per_doc=50
max_size_per_field=500
stats_frequency=30

host=https://10.10.33.101:9200
username=elastic
password=Passw0Rd!

python3 es-perf-test.py --es_ip $host \
        --indices $indices --documents $documents \
        --client_conn $clients --duration $seconds \
        --shards $shards \
        --replicas $replicas \
        --bulk_number $bulk_size \
        --max-fields-per-document $max_fields_per_doc \
        --max-size-per-field $max_size_per_field \
        --stats-frequency $stats_frequency \
        --user $username \
        --pass $password \
        --no-verify
