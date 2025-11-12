# Поиск, автодополнение, подсказки

from elasticsearch import Elasticsearch, helpers
from models import ARTISTS_DATA, SONGS_DATA, ALBUMS_DATA, GENRES_DATA
from mappings import artists_mapping, songs_mapping, albums_mapping, genres_mapping

def init_elasticsearch_data(es: Elasticsearch):
    """
    Инициализация всех индексов и загрузка данных в Elasticsearch.
    Удаляет старые индексы, создаёт новые и индексирует объекты из models.
    """
    indices = {
        "artists": (artists_mapping, ARTISTS_DATA, "artist_id"),
        "songs": (songs_mapping, SONGS_DATA, "song_id"),
        "albums": (albums_mapping, ALBUMS_DATA, "album_id"),
        "genres": (genres_mapping, GENRES_DATA, "genre_id"),
    }

    for index_name, (mapping, data, id_field) in indices.items():
        # --- 1. Удаляем старый индекс, если есть
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            print(f"Удалён старый индекс: {index_name}")

        # --- 2. Создаём новый индекс
        es.indices.create(index=index_name, body=mapping)
        print(f"Создан новый индекс: {index_name}")

        # --- 3. Загружаем данные
        if data:
            actions = []
            for obj in data:
                obj_dict = obj.to_dict()
                actions.append({
                    "_index": index_name,
                    "_id": obj_dict[id_field],
                    "_source": obj_dict,
                })

            helpers.bulk(es, actions)
            print(f"📦 Загружено {len(actions)} документов в {index_name}")

    print("🎉 Инициализация Elasticsearch завершена успешно!")



INDEX_NAME = "artists"


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


# ======== SONGS ========
def search_songs(es, query: str, page: int = 1, size: int = 10):
    """Поиск песен с пагинацией и исправлением опечаток"""
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name^2", "file_url"],
                "fuzziness": "AUTO"
            }
        },
        "from": (page - 1) * size,
        "size": size
    }

    res = es.search(index="songs", body=body)

    return {
        "total": res["hits"]["total"]["value"],
        "page": page,
        "size": len(res["hits"]["hits"]),
        "results": [hit["_source"] for hit in res["hits"]["hits"]]
    }


# ======== ALBUMS ========
def search_albums(es, query: str, page: int = 1, size: int = 10):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name^2", "cover_art_url"],
                "fuzziness": "AUTO"
            }
        },
        "from": (page - 1) * size,
        "size": size
    }
    res = es.search(index="albums", body=body)
    return {
        "total": res["hits"]["total"]["value"],
        "page": page,
        "size": len(res["hits"]["hits"]),
        "results": [hit["_source"] for hit in res["hits"]["hits"]]
    }


# ======== GENRES ========
def search_genres(es, query: str, page: int = 1, size: int = 10):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name^2"],
                "fuzziness": "AUTO"
            }
        },
        "from": (page - 1) * size,
        "size": size
    }
    res = es.search(index="genres", body=body)
    return {
        "total": res["hits"]["total"]["value"],
        "page": page,
        "size": len(res["hits"]["hits"]),
        "results": [hit["_source"] for hit in res["hits"]["hits"]]
    }
