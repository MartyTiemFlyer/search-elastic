from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, RequestError
from models import ARTISTS_DATA
from mappings import artists_mapping
from search import init_elasticsearch_data, search_artists, suggest_artists
print("🚀 Search Service STARTED!", flush=True)

ES_HOST = "http://localhost:9200"
INDEX_NAME = "artists"
app = Flask(__name__)

es = Elasticsearch(ES_HOST, verify_certs=False)

def delete_artists_index():
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Индекс '{INDEX_NAME}' удалён.")
    else:
        print(f"Индекс '{INDEX_NAME}' не найден.")

def load_sample_artists():
    for artist in ARTISTS_DATA:
        doc = artist.to_dict()
        # добавляем поле для автодополнения
        doc["name_suggest"] = {"input": [artist.name]}
        es.index(index=INDEX_NAME, id=artist.artist_id, body=doc)

    print(f"Загружено {len(ARTISTS_DATA)} артистов в индекс '{INDEX_NAME}'.")



def create_artists_index():
    if es.indices.exists(index=INDEX_NAME):
        print(f"Индекс '{INDEX_NAME}' уже существует.")
        return

    try:
        es.indices.create(index=INDEX_NAME, body=artists_mapping)
        print(f"Индекс '{INDEX_NAME}' создан успешно.")
    except RequestError as e:
        print(f"Ошибка при создании индекса: {e.info}")


# ======== Утилита для формирования стандартизированного ответа ========
def make_response(data, query="", page=1, total=0, status="ok", message=None):
    return {
        "status": status,
        "query": query,
        "page": page,
        "size": len(data),
        "total": total,
        "data": data,
        "message": message
    }

# ======== Поиск артистов ========
@app.route("/search")
def search():
    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))

    if not query:
        return jsonify(make_response([], query, page, 0, status="error", message="Пустой запрос")), 400

    results_obj = search_artists(es, query, page, size)
    response = make_response(
        data=results_obj["results"],
        query=query,
        page=page,
        total=results_obj["total"]
    )
    return jsonify(response)

# ======== Автодополнение артистов ========
@app.route("/suggest")
def suggest():
    prefix = request.args.get("q", "")
    size = int(request.args.get("size", 5))

    if not prefix:
        return jsonify(make_response([], prefix, 1, 0, status="error", message="Пустой запрос")), 400

    suggestions_obj = suggest_artists(es, prefix, size)
    response = make_response(
        data=suggestions_obj["suggestions"],
        query=prefix,
        page=1,
        total=suggestions_obj["total"]
    )
    return jsonify(response)



if __name__ == "__main__":
    #delete_artists_index()
    #create_artists_index()
    #load_sample_artists()

    #init_elasticsearch_data(es)
    #
    #results = search_artists(es, "adel")
    #for r in results:
    #    print(f"{r['name']} — {r['artist_biography']}")
    #print("--- все результаты показаны ---")
    #
    #suggestions = suggest_artists(es, "R")
    #print(suggestions)
    app.run(debug=True)
