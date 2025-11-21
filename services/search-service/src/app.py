from flask import Flask, request, jsonify, send_from_directory
from elasticsearch import Elasticsearch, RequestError
from models import ARTISTS_DATA
from mappings import artists_mapping, genres_mapping, albums_mapping, songs_mapping
from search import init_elasticsearch_data, search_albums, search_artists, search_genres, search_songs, suggest_artists
print("🚀 Search Service STARTED!", flush=True)

ES_HOST = "http://elasticsearch:9200"
INDEX_NAME = "artists"
app = Flask(__name__)

es = Elasticsearch(ES_HOST, basic_auth=("elastic", "elastic"))


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

# ======== Home Start ========
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# ======== Поиск артистов ========
@app.route("/search")
def search():
    query = request.args.get("q", "")
    type_ = request.args.get("type", "artists")
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))

    if not query:
        return jsonify(make_response([], query, page, 0, status="error", message="Пустой запрос")), 400

    # выбираем нужную функцию
    if type_ == "songs":
        results_obj = search_songs(es, query, page, size)
    elif type_ == "albums":
        results_obj = search_albums(es, query, page, size)
    elif type_ == "genres":
        results_obj = search_genres(es, query, page, size)
    else:
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

@app.route("/search_all")
def search_all():
    query = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))  # кол-во на категорию

    if not query:
        return jsonify(make_response({}, query, page, 0, status="error", message="Пустой запрос")), 400

    results = {
        "artists": search_artists(es, query, page, size)["results"],
        "songs": search_songs(es, query, page, size)["results"],
        "albums": search_albums(es, query, page, size)["results"],
        "genres": search_genres(es, query, page, size)["results"],
    }

    total = sum(len(v) for v in results.values())

    response = make_response(
        data=results,
        query=query,
        page=page,
        total=total
    )
    return jsonify(response)


if __name__ == "__main__":
    #load_sample_artists()

    init_elasticsearch_data(es)
    
    #results = search_artists(es, "adel")
    #for r in results:
    #    print(f"{r['name']} — {r['artist_biography']}")
    #print("--- все результаты показаны ---")
    #
    #suggestions = suggest_artists(es, "R")
    #print(suggestions)
    app.run(debug=True)
