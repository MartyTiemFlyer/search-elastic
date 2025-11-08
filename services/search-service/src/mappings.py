# схемы индексов (settings + mappings)

artists_mapping = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
      "tokenizer": {
        "edge_ngram_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 20,
          "token_chars": ["letter", "digit", "whitespace"]
        }
      },
      "analyzer": {
        "edge_ngram_analyzer": {
          "tokenizer": "edge_ngram_tokenizer",
          "filter": ["lowercase"]
        },
        "lowercase_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "artist_id": { "type": "long" },
      "name": {
        "type": "text",
        "analyzer": "lowercase_analyzer",
        "fields": {
          "ngram": {
            "type": "text",
            "analyzer": "edge_ngram_analyzer",
            "search_analyzer": "lowercase_analyzer"
          }
        }
      },
      "name_suggest": { "type": "completion" },
      "artist_biography": { "type": "text" }
    }
  }
}

