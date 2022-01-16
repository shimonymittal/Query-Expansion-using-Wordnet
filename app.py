from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from nltk.corpus import wordnet as wn
import os
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
CORS(app)
es = Elasticsearch()
result = {}

@app.route('/fetch', methods=['GET'])
def helloworld():
    q = request.args.get('q', default="", type=str)
    data = {'hi': 'bye'}
    resp = es.search(index="my_index", query={"combined_fields": {"query": get_synomys(q),
                                                                  "fields": ["title", "content"]}}, highlight={
        "pre_tags": ["<b>"],
        "post_tags": ["</b>"],
        "fields": {
            "content": {}
        }
    })
    if(request.method == 'GET'):
        return jsonify(resp)



def get_synomys(query):
    query_words = query.split(" ")
    query_syms = set()
    for word in query_words:
        query_syms.add(word)
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                query_syms.add(l.name().split(".")[0])
            for l in syn.hypernyms():
                query_syms.add(l.name().split(".")[0])
            for l in syn.hyponyms():
                query_syms.add(l.name().split(".")[0])

    return " ".join(query_syms)


def check_elastic_active():
    client = Elasticsearch()


if __name__ == "__main__":
    app.run(debug=True, port=8000)
