curl -XPUT -k 'https://127.0.0.1:9200/bom'\
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
        "aifstime_utc": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "air_temp": {
            "type": "float"
        },
        "apparent_t": {
            "type": "float"
        },
        "cloud": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "cloud_base_m": {
            "type": "float"
        },
        "cloud_oktas": {
            "type": "float"
        },
        "cloud_type": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "cloud_type_id": {
            "type": "float"
        },
        "delta_t": {
            "type": "float"
        },
        "dewpt": {
            "type": "float"
        },
        "gust_kmh": {
            "type": "long"
        },
        "gust_kt": {
            "type": "long"
        },
        "history_product": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "lat": {
            "type": "float"
        },
        "local_date_time": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "local_date_time_full": {
            "type": "date",
            "format": "yyyyMMddHHmmss"
        },
        "lon": {
            "type": "float"
        },
        "name": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "press": {
            "type": "float"
        },
        "press_msl": {
            "type": "float"
        },
        "press_qnh": {
            "type": "float"
        },
        "press_tend": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "rain_trace": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "rel_hum": {
            "type": "long"
        },
        "sea_state": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "sort_order": {
            "type": "long"
        },
        "swell_dir_worded": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "swell_height": {
            "type": "float"
        },
        "swell_period": {
            "type": "long"
        },
        "vis_km": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "weather": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "wind_dir": {
            "type": "text",
            "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
            }
        },
        "wind_spd_kmh": {
            "type": "long"
        },
        "wind_spd_kt": {
            "type": "long"
        },
        "wmo": {
            "type": "long"
        }
        }

    }\
   --user 'elastic:elastic' | jq '.'
