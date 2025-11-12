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


genres_mapping = {
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
      "genre_id": { "type": "integer" },
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
      "name_suggest": { "type": "completion" }
    }
  }
}


albums_mapping = {
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
      "album_id": { "type": "long" },
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
      "release_date": { "type": "date" },
      "cover_art_url": { "type": "keyword" },
      "disc_count": { "type": "integer" },
      "artist_id": { "type": "long" },
      "genre_id": { "type": "integer" }
    }
  }
}


songs_mapping = {
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
      "song_id": { "type": "long" },
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
      "track_number_album": { "type": "integer" },
      "disc_number": { "type": "integer" },
      "duration": { "type": "integer" },
      "file_url": { "type": "keyword" },
      "artist_id": { "type": "long" },
      "album_id": { "type": "long" }
    }
  }
}
