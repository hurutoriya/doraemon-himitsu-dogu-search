FROM docker.elastic.co/elasticsearch/elasticsearch:8.4.3
# set the specific password for Elasticsearch
RUN echo "elastic" | bin/elasticsearch-keystore add "bootstrap.password" -xf