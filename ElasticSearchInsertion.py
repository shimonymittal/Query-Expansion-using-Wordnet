from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from nltk.corpus import wordnet as wn
import nltk
import os
from flask import Flask, render_template,request



def check_elastic_active():
    client = Elasticsearch()
    resp = client.info()
    print(resp)


def create_index(client):
    """ Creates an index in Elasticsearch if one isn't already there. """

    client.indices.create(
        index="my_index",
        settings={"number_of_shards": 1,
                  "highlight.max_analyzed_offset": 60000000,
                  "analysis": {
                      "analyzer": {
                          "my_english_analyzer": {
                              "tokenizer": "standard",
                              "filter": [
                                  "lowercase",
                                  "stop",
                                  "snowball"
                              ]
                          }
                      }
                  }
                  },
        mappings={
            "properties": {
                "title": {"type": "text",
                          "analyzer": "my_english_analyzer",
                          "search_analyzer": "my_english_analyzer"},
                "content": {"type": "text",
                            "analyzer": "my_english_analyzer",
                            "search_analyzer": "my_english_analyzer"}
            },
        },
        ignore=400,
    )


def generate_actions():
    """ Reads through each file in the folder. This function is passed into the bulk()
    helper to create many documents in sequence. """

    path = os.getcwd()
    path = path + "\Ten_Doclist"
    all_files = os.listdir(path)

    os.chdir(path)

    i = 0

    for file in all_files:
        i += 1
        with open(file) as f:
            lines = f.readlines()

        doc = {
            "_id": i,
            "title": file,
            "content": lines
        }

        yield doc


es = Elasticsearch()

create_index(es)

for ok, response in streaming_bulk(
        client=es, index="my_index", actions=generate_actions(),
):
    if not ok:
        print(response)


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

res = es.search(index="my_index", query={"combined_fields": {"query": get_synomys("baddie's the villain"),
                                                                  "fields": ["title", "content"]}}, highlight={
    "pre_tags": ["<b>"],
    "post_tags": ["</b>"],
    "fields ": {
        "content": {}
    }
})

print(res)
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print(" %(title)s: %(content)s" % hit["_source"])
    print('----------HIGHLIGHTSSS ------------------')
    print(f"{hit['_source']['title']} : {hit['highlight']}")
    print(hit["_score"])
    print('----------------------------------------------')


