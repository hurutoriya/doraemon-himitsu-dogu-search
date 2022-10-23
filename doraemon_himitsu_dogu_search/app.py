import pandas as pd
import sentents_bert
import streamlit as st
from elasticsearch import Elasticsearch

from data import (
    CERT_PATH,
    ELASTIC_PASSWORD,
    ELASTIC_USER,
    ENDPOINT,
    INDEX_NAME,
    MODEL_NAME,
)

def main():
    es = Elasticsearch(
        ENDPOINT,
        ca_certs=CERT_PATH,
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    )

    st.write("ドラえもんひみつ道具検索エンジン")
    st.text_input("検索キーワード (探したい道具の説明を入れてね)", key="name", placeholder="空を飛べる")

    model = sentents_bert.SentenceBertJapanese(MODEL_NAME)
    sentence_embeddings = model.encode([st.session_state.name], batch_size=1)
    sentence_embeddings = sentence_embeddings.cpu().detach().numpy().tolist()

    query = {
        "knn": {
            "field": "vector",
            "query_vector": sentence_embeddings[0],
            "k": 10,
            "num_candidates": 100,
        },
        "fields": ["name", "description"],
    }
    result = es.search(index=INDEX_NAME, body=query)

    serp = [ {
                "似ている度": document["_score"],
                "ひみつ道具の名前": document["_source"]["name"],
                "よみかた": document["_source"]["yomi"],
                "説明": document["_source"]["description"],
            } for document in result["hits"]["hits"]]

    st.table(pd.DataFrame(serp))

if __name__ == "__main__":
    main()