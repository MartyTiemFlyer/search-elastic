# Поиск, автодополнение, подсказки

from elasticsearch import Elasticsearch
from models import ARTISTS_DATA

INDEX_NAME = "artists"


def init_elasticsearch_data(es: Elasticsearch):
    """Создает индекс artists и заполняет его тестовыми данными."""
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    es.indices.create(
        index=INDEX_NAME,
        body={
            "mappings": {
                "properties": {
                    "artist_id": {"type": "integer"},
                    "name": {"type": "text"},
                    "artist_biography": {"type": "text"},
                }
            }
        }
    )

    for artist in ARTISTS_DATA:
        es.index(index=INDEX_NAME, id=artist.artist_id, document=artist.to_dict())

    es.indices.refresh(index=INDEX_NAME)
    print(f"Индекс '{INDEX_NAME}' успешно создан и заполнен {len(ARTISTS_DATA)} документами.")


# --- ARTIST ---
def search_artists(es, query: str, page: int = 1, size: int = 10):
    """Поиск артистов с поддержкой пагинации и исправлением опечаток."""
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name^2", "artist_biography"],
                "fuzziness": "AUTO"
            }
        },
        "from": (page - 1) * size,
        "size": size
    }

    res = es.search(index="artists", body=body)

    return {
        "total": res["hits"]["total"]["value"],
        "page": page,
        "size": len(res["hits"]["hits"]),
        "results": [hit["_source"] for hit in res["hits"]["hits"]]
    }



def suggest_artists(es, prefix: str, size: int = 5):
    """Автодополнение по имени артиста с JSON-ответом."""
    if not prefix:
        return {"query": prefix, "size": 0, "suggestions": []}

    response = es.search(
        index="artists",
        query={
            "prefix": {"name": prefix.lower()}
        },
        size=size
    )

    suggestions = [hit["_source"]["name"] for hit in response["hits"]["hits"]]

    return {
        "query": prefix,
        "size": len(suggestions),
        "total": response["hits"]["total"]["value"],
        "suggestions": suggestions
    }
