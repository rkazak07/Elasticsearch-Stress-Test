import argparse
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
import random
import time
import ssl
import psutil
import os 

# Argümanları ayrıştırma
parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default="localhost", help="Elasticsearch sunucu adresi")
parser.add_argument("--port", type=str, default="9200", help="Elasticsearch sunucu portu")
parser.add_argument("--index", type=str, default="test-index", help="Index adı")
parser.add_argument("--num-docs", type=int, default=1000, help="Oluşturulacak belge sayısı")
parser.add_argument("--batch-size", type=int, default=100, help="Toplu işleme boyutu")
parser.add_argument("--num-queries", type=int, default=1000, help="Yapılacak sorgu sayısı")
parser.add_argument("--query-size", type=int, default=10, help="Sorgu boyutu")
parser.add_argument("--num-threads", type=int, default=1, help="Çalışacak iş parçacığı sayısı")
parser.add_argument("--username", type=str, default=None, help="Elasticsearch kullanıcı adı")
parser.add_argument("--password", type=str, default=None, help="Elasticsearch parola")
parser.add_argument("--duration", type=int, default=60, help="Testin çalışma süresi (saniye cinsinden)")

args = parser.parse_args()

# SSL sertifikası ayarları
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Elasticsearch istemcisini oluşturma
if args.username and args.password:
    es = Elasticsearch(
        hosts=[{"host": args.host, "port": args.port}],
        http_auth=(args.username, args.password),
        use_ssl=True,
        ssl_context=ssl_context,
        connection_class=RequestsHttpConnection
    )
else:
    es = Elasticsearch(hosts=[args.host])

# Rastgele belgeler oluşturma
def generate_docs(num_docs):
    for i in range(num_docs):
        yield {
            "_index": args.index,
            "_source": {
                "title": f"Belge {i}",
                "body": f"Bu, {i}. belgenin gövdesidir."
            }
        }
        if (i+1) % 100 == 0:
            print(f"{i+1} belge oluşturuldu ve diske yazıldı.", flush=True)
			
# Belge verilerini Elasticsearch'e yükleme
def bulk_index_docs(es, docs, batch_size):
    success_count = 0
    error_count = 0
    start_time = time.time()
    for success, info in es.bulk((doc for doc in docs), index=args.index, chunk_size=batch_size, raise_on_error=True):
        if success:
            success_count += 1
        else:
            error_count += 1
        # Her batch_size işleminden sonra CPU, RAM, disk kullanımı bilgisini al
        if (success_count + error_count) % batch_size == 0:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            print(f"Processed {success_count+error_count} docs - CPU: {cpu_percent}% - Memory: {memory_percent}% - Disk usage: {disk_usage}%")
    end_time = time.time()
    total_time = end_time - start_time
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    print(f"Processed {success_count+error_count} docs in {total_time:.2f} seconds - CPU: {cpu_percent}% - Memory: {memory_percent}% - Disk usage: {disk_usage}%")
    return success_count, error_count

# Belge sayısı ve toplam boyutunu hesaplama
def calculate_index_stats(es):
    stats = es.indices.stats(index=args.index)
    num_docs = stats["indices"][args.index]["total"]["docs"]["count"]
    total_size = stats["indices"][args.index]["total"]["store"]["size_in_bytes"]
    return num_docs, total_size

# Sorgu verilerini oluşturma
def generate_queries(num_queries, query_size):
    for i in range(num_queries):
        yield {
            "size": query_size,
            "query": {
                "match": {
                    "body": f"belge {random.randint(0, args.num_docs-1)}"
                }
            }
        }

# Sorgu isteklerini Elasticsearch'e gönderme
def search(es, queries):
    total_hits = 0
    total_time = 0
    for query in queries:
        res = es.search(index=args.index, body=query)
        total_hits += res["hits"]["total"]["value"]
        total_time += res["took"]
    return total_hits, total_time
	
start_time = time.monotonic()
while time.monotonic() - start_time < args.duration:
    # test kodları
