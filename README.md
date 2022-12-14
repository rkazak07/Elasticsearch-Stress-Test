# Elasticsearch Stress Test

### Overview
This script generates a bunch of documents, and indexes as much as it can to Elasticsearch. While doing so, it prints out metrics to the screen to let you follow how your cluster is doing. Also this project supports working elasticsearch up to version 7.17.7

### Note
* If you constantly receive a failed error even though the Elasticsearch server has a low resource usage. Review the resource usage of the computer on which you perform the operation.

### How to use
* Download this project
* Change script
* Make sure you have Python 3.6+
* pip install elasticsearch7  


### How does it work
The script creates document templates based on your input. Say - 5 different documents.
The documents are created without fields, for the purpose of having the same mapping when indexing to ES.
After that, the script takes 10 random documents out of the template pool (with redraws) and populates them with random data.

After we have the pool of different documents, we select an index out of the pool, select documents * bulk size out of the pool, and index them.

The generation of documents is being processed before the run, so it will not overload the server too much during the benchmark.

### Mandatory Parameters
| Parameter | Description |
| --- | --- |
| `--es_ip` | Address of the Elasticsearch cluster (no protocol and port). You can supply mutiple clusters here, but only **one** node in each cluster (preferably the client node) |
| `--indices` | Number of indices to write to |
| `--documents` | Number of template documents that hold the same mapping |
| `--client_conn` | Number of threads that send bulks to ES |
| `--duration` | How long should the test run. Note: it might take a bit longer, as sending of all bulks whose creation has been initiated is allowed |


### Optional Parameters
| Parameter | Description | Default
| --- | --- | --- |
| `--shards` | How many shards per index |3|
| `--replicas` | How many replicas per index |1|
| `--bulk_number` | How many documents each bulk request should contain |500|
| `--max-fields-per-document` | What is the maximum number of fields each document template should hold |100|
| `--max-size-per-field` | When populating the templates, what is the maximum length of the data each field would get |1000|
| `--no-cleanup` | Boolean field. Don't delete the indices after completion |False|
| `--stats-frequency` | How frequent to show the statistics |30|
| `--not-green` | Script doesn't wait for the cluster to be green |False|
| `--no-verify` | No verify SSL certificates|False|
| `--ca-file` | Path to Certificate file ||
| `--user` | Basic authentication Username ||
| `--pass` | Basic authentication Password ||




### Examples
> Run the test for 2 Elasticsearch clusters, with 4 indices on each, 5 random documents, don't wait for the cluster to be green, open 5 different writing threads run the script for 120 seconds
```bash
python es-perf-test.py  --es_ip http://10.10.33.100:9200 http://10.10.33.101:9200 --indices 4 --documents 5 --duration 120 --not-green --client_conn 5
```

> Run the test on ES cluster 10.10.33.100, with 10 indices, 10 random documents with up to 10 fields in each, the size of each field on each document can be up to 50 chars, each index will have 1 shard and no replicas, the test will run from 1 client (thread) for 300 seconds, will print statistics every 15 seconds, will index in bulks of 5000 documents  will leave everything in Elasticsearch after the test
```bash
 python es-perf-test.py --es_ip http://10.10.33.100 --indices 10 --documents 10 --client_conn 1 --duration 300 --shards 1 --replicas 0 --bulk_number 5000 --max-fields-per-document 10 --max-size-per-field 50 --no-cleanup --stats-frequency 15
```

> Run the test with SSL
```bash
 python es-perf-test.py --es_ip https://10.10.33.101:9200 --indices 5 --documents 5 --client_conn 2  --duration 120 --ca-file /path/ca.pem
```

> Run the test with SSL without verify the certificate
```bash
 python es-perf-test.py --es_ip https://10.10.33.101:9200 --indices 5 --documents 5 --client_conn 1 --duration 120 --no-verify
```

> Run the test with HTTP Authentification
```bash
 python es-perf-test.py --es_ip 10.10.33.100 --indices 5 --documents 5 --client_conn 1 --duration 120 --user username --pass changeme
```

### Example Output

> Run the test  Opensearch cluster on rhel8  , with 5 indices on each, 5 random documents, don't wait for the cluster to be green, with SSL without verify the certificate, open 2 different writing threads run the script for 60 seconds
```bash
 [root@Node elastic-perf]# sh es-perf.sh

Starting initialization of https://10.10.33.100:9200
Done!
Creating indices..
Generating documents and workers..
Done!
Starting the test. Will print stats every 30 seconds.
The test would run for 60 seconds, but it might take a bit more because we are waiting for current bulk operation to complete.

Elapsed time: 31 seconds
Successful bulks: 328 (164000 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 734.9789419174194 MB which is 23.71 MB/s


Test is done! Final results:
Elapsed time: 60 seconds
Successful bulks: 749 (374500 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 1674.2647771835327 MB which is 27.90 MB/s

Cleaning up created indices..
Done!

```


### Docker Installation

> Build Docker images
```bash
 docker build -t rkazak1/es-perf-test:v1 .
```
> While running the Docker image, revise the parameters according to your system.
```bash
 docker run -t -i rkazak1/es-perf-test:v1 --es_ip <https://ip:port> \
--indices <indices number> --documents <document number> \
--client_conn <client number> --duration <duration> \
--shards <shards number> --bulk_number <bulk number> \
--user <username> \
--pass <password> \
--no-verify \
--not-green
```

### Docker Example

> Run the test on ES cluster 10.10.33.100, with 5 indices, 5 random documents with up to 20 fields in each, the size of each field on each document can be up to 5 chars, each index will have 1 shard and no replicas, the test will run from 2 client (thread) for 100 seconds, will print statistics every 15 seconds, will index in bulks of 500 documents  will leave everything in Elasticsearch after the test 

```bash

 [root@Node elastic-perf]# docker run -t -i rkazak/es-perf-test:v1 --es_ip http://10.10.33.100:9200 \ 
 > --indices 5 --documents 5 \
 > --client_conn 2 --duration 100 \
 > --shards 1 --replicas 0 \
 > --bulk_number 500 \
 > --max-fields-per-document 5 --max-size-per-field 20 \
 > --no-cleanup --stats-frequency 15

Starting initialization of http://10.10.33.100:9200
Done!
Creating indices..
Generating documents and workers..
Done!
Starting the test. Will print stats every 15 seconds.
The test would run for 100 seconds, but it might take a bit more because we are waiting for current bulk operation to complete.

Elapsed time: 16 seconds
Successful bulks: 1262 (631000 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 65.48140811920166 MB which is 4.09 MB/s

Elapsed time: 31 seconds
Successful bulks: 2786 (1393000 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 144.54638767242432 MB which is 4.66 MB/s

Elapsed time: 46 seconds
Successful bulks: 4404 (2202000 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 228.4937391281128 MB which is 4.97 MB/s

Elapsed time: 61 seconds
Successful bulks: 5933 (2966500 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 307.81461334228516 MB which is 5.05 MB/s

Elapsed time: 76 seconds
Successful bulks: 7434 (3717000 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 385.68299102783203 MB which is 5.07 MB/s

Elapsed time: 91 seconds
Successful bulks: 9067 (4533500 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 470.3853235244751 MB which is 5.17 MB/s


Test is done! Final results:
Elapsed time: 100 seconds
Successful bulks: 10001 (5000500 documents)
Failed bulks: 0 (0 documents)
Indexed approximately 518.8512392044067 MB which is 5.19 MB/s


```
