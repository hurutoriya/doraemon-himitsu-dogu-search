import json

import numpy as np
from elasticsearch import Elasticsearch
from tqdm import tqdm

from data import (
    CERT_PATH,
    ELASTIC_PASSWORD,
    ELASTIC_USER,
    ENDPOINT,
    HIMITSU_DOGU_DATA_PATH,
    INDEX_NAME,
    MAPPING_PATH,
    SENTENTS_VECTOR_DATA_PATH,
)

if __name__ == "__main__":

    himitsu_dogu_sentents_vectors = np.load(SENTENTS_VECTOR_DATA_PATH)

    with open(HIMITSU_DOGU_DATA_PATH, "r") as f:
        himitsu_dogus = json.load(f)

    # NOTE: Elasticsaerch mapping definition
    with open(MAPPING_PATH, "r") as f:
        mapping = json.load(f)

    # Create the client instance
    es = Elasticsearch(
        ENDPOINT,
        ca_certs=CERT_PATH,
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    )

    es.indices.create(index=INDEX_NAME, body=mapping)

    for himitsu_dogu, vector in tqdm(zip(himitsu_dogus, himitsu_dogu_sentents_vectors)):
        himitsu_dogu["vector"] = vector.tolist()
        resp = es.index(index=INDEX_NAME, id=himitsu_dogu["id"], document=himitsu_dogu)
