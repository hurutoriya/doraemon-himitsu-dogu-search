"""Shared params."""

# NOTE: Elasticsearch
ELASTIC_USER = "elastic"
ELASTIC_PASSWORD = "elastic"
CERT_PATH = "http_ca.crt"
ENDPOINT = "https://localhost:9200"
INDEX_NAME = "himitsu_dogu"
MAPPING_PATH = "data/input/ann_mapping.json"
# NOTE: Data path
SENTENTS_VECTOR_DATA_PATH: str = "data/output/himitsu_dogu_sentens_vector.npy"
HIMITSU_DOGU_RAW_DATA_PATH: str = "./data/raw/himitsu-dogu.txt"
HIMITSU_DOGU_DATA_PATH = "data/input/docs.json"
# NOTE: Hugging face model name
MODEL_NAME = "sonoisa/sentence-bert-base-ja-mean-tokens-v2"
