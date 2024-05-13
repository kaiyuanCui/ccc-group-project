curl -XPUT -k 'https://127.0.0.1:9200/epa'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "siteID": {
                "type": "keyword"
            },
            "siteName": {
                "type": "text"
            },
            "siteType": {
                "type": "keyword"
            },
            "geometry": {
                "type": "geo_shape"
            },
            "siteHealthAdvices": {
                "type": "nested",
                "properties": {
                    "since": {
                        "type": "date"
                    },
                    "until": {
                        "type": "date"
                    },
                    "healthParameter": {
                        "type": "keyword"
                    },
                    "averageValue": {
                        "type": "scaled_float",
                        "scaling_factor": 100
                    },
                    "unit": {
                        "type": "keyword"
                    },
                    "healthAdvice": {
                        "type": "keyword"
                    },
                    "healthAdviceColor": {
                        "type": "keyword"
                    },
                    "healthCode": {
                        "type": "keyword"
                    }
                }
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
