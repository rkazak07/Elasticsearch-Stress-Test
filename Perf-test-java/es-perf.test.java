import java.util.Random;
import java.util.concurrent.TimeUnit;
import org.apache.http.HttpHost;
import org.elasticsearch.action.bulk.BulkRequest;
import org.elasticsearch.action.bulk.BulkResponse;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.builder.SearchSourceBuilder;

public class ElasticsearchLoadTester {
    
    public static void main(String[] args) throws Exception {
        
        // Argümanları ayrıştırma
        String host = "localhost";
        String port = "9200";
        String index = "test-index";
        int numDocs = 1000;
        int batchSize = 100;
        int numQueries = 1000;
        int querySize = 10;
        int numThreads = 1;
        String username = null;
        String password = null;
        int duration = 60;
        
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--host":
                    host = args[++i];
                    break;
                case "--port":
                    port = args[++i];
                    break;
                case "--index":
                    index = args[++i];
                    break;
                case "--num-docs":
                    numDocs = Integer.parseInt(args[++i]);
                    break;
                case "--batch-size":
                    batchSize = Integer.parseInt(args[++i]);
                    break;
                case "--num-queries":
                    numQueries = Integer.parseInt(args[++i]);
                    break;
                case "--query-size":
                    querySize = Integer.parseInt(args[++i]);
                    break;
                case "--num-threads":
                    numThreads = Integer.parseInt(args[++i]);
                    break;
                case "--username":
                    username = args[++i];
                    break;
                case "--password":
                    password = args[++i];
                    break;
                case "--duration":
                    duration = Integer.parseInt(args[++i]);
                    break;
                default:
                    System.err.println("Invalid argument: " + args[i]);
                    System.exit(1);
            }
        }
        
        // Elasticsearch istemcisini oluşturma
        RestHighLevelClient client;
        if (username != null && password != null) {
            client = new RestHighLevelClient(
                RestClient.builder(
                    new HttpHost(host, Integer.parseInt(port), "https")
                ).setHttpClientConfigCallback(httpClientBuilder -> {
                    return httpClientBuilder.setDefaultCredentialsProvider(
                        new BasicCredentialsProvider() {{
                            setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(username, password));
                        }}
                    ).setSSLContext(SSLContext.getDefault());
                })
            );
        } else {
            client = new RestHighLevelClient(
                RestClient.builder(
                    new HttpHost(host, Integer.parseInt(port), "http")
                )
            );
        }
        
        // Rastgele belgeler oluşturma
        Random random = new Random();
        BulkRequest bulkRequest = new BulkRequest();
        for (int i = 0; i < numDocs; i++) {
            bulkRequest.add(
                new IndexRequest(index)
                    .source(
                        XContentType.JSON,
                        "title", "Belge " + i,
                        "body", "Bu, " + i + ". belgenin gövdesidir."
                    )
            );
            if ((i+1) % 100 == 0) {
                BulkResponse bulkResponse =
