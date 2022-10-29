import pandas as pd
import sentents_bert
import streamlit as st
from elasticsearch import Elasticsearch

from data import CERT_PATH, ELASTIC_PASSWORD, ELASTIC_USER, ENDPOINT, INDEX_NAME, MODEL_NAME


def main():
    es = Elasticsearch(
        ENDPOINT,
        ca_certs=CERT_PATH,
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    )

    st.write("ドラえもんひみつ道具検索エンジン")
    st.text_input("検索キーワード (探したい道具の説明を入れてね)", key="query")

    model = sentents_bert.SentenceBertJapanese(MODEL_NAME)
    sentence_embeddings = model.encode([st.session_state.query], batch_size=1)
    sentence_embeddings = sentence_embeddings.cpu().detach().numpy().tolist()

    TOP_K: int = 10

    multimatch_query: dict = {
        "size": TOP_K,
        "query": {"multi_match": {"query": st.session_state.query, "fields": ["name", "description"]}},
    }
    ann_query: dict = {
        "knn": {
            "field": "vector",
            "query_vector": sentence_embeddings[0],
            "k": TOP_K,
            "num_candidates": 100,
        }
    }
    # NOTE: score = match score + ann score
    hybrid_query: dict = {
        "size": TOP_K,
        "query": {"multi_match": {"query": st.session_state.query, "fields": ["name", "description"]}},
        "knn": {
            "field": "vector",
            "query_vector": sentence_embeddings[0],
            "k": TOP_K,
            "num_candidates": 100,
        },
    }

    multimatch_result = es.search(index=INDEX_NAME, body=multimatch_query)
    ann_result = es.search(index=INDEX_NAME, body=ann_query)
    hybrid_result = es.search(index=INDEX_NAME, body=hybrid_query)
    multimatch_serp: dict = [
        {
            "スコア": document["_score"],
            "ひみつ道具の名前": document["_source"]["name"],
            "説明": document["_source"]["description"],
        }
        for document in multimatch_result["hits"]["hits"]
    ]
    ann_serp: dict = [
        {
            "スコア": document["_score"],
            "ひみつ道具の名前": document["_source"]["name"],
            "説明": document["_source"]["description"],
        }
        for document in ann_result["hits"]["hits"]
    ]
    hybrid_serp: dict = [
        {
            "スコア": document["_score"],
            "ひみつ道具の名前": document["_source"]["name"],
            "説明": document["_source"]["description"],
        }
        for document in hybrid_result["hits"]["hits"]
    ]

    df_multimatch = pd.DataFrame(multimatch_serp)
    df_ann = pd.DataFrame(ann_serp)
    df_hybrid = pd.DataFrame(hybrid_serp)

    # NOTE: change to 1 orign in index
    df_multimatch.index = df_multimatch.index + 1
    df_ann.index = df_ann.index + 1
    df_hybrid.index = df_hybrid.index + 1

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header(f"Multi match: {len(df_multimatch)}hit")
        st.table(df_multimatch)
    with col2:
        st.header(f"ANN: {len(df_ann)}hit")
        st.table(df_ann)
    with col3:
        st.header(f"Hybrid: {len(df_hybrid)}hit")
        st.table(df_hybrid)


if __name__ == "__main__":
    main()
