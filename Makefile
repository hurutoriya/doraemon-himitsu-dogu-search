# Target source file
SRC=doraemon_himitsu_dogu_search

.PHONY: lint
lint:
	@echo "Run Linter"
	poetry run flake8 .
	poetry run black . --check
	poetry run mypy .
	poetry run isort . --check

.PHONY: fmt
fmt:
	@echo "Run formatter"
	poetry run black .
	poetry run isort .

.PHONY: run-es
run-es:
	@docker rm es01
	@docker build --tag=es .
	@docker run --name es01 --net elastic -p 9200:9200 -p 9300:9300 -it -v /usr/share/elasticsearch/data es

.PHONY: get-es-cert
get-es-cert: 
	@echo "Get the certification for ElasticSearch"
	@docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .

.PHONY: build-index
build-index: get-es-cert
	@echo "Make structured data from raw data"
	poetry run python $(SRC)/preprocess.py
	@echo "Run sentens vectorizer"
	poetry run python $(SRC)/sentents_bert_vectorizer.py
	@echo "Run Elasticsearch indexing job"
	poetry run python $(SRC)/indexer.py

.PHONY: es-info
es-info: get-es-cert
	@echo "Show the running Elasticsearch info"
	curl --cacert http_ca.crt -u elastic:elastic https://localhost:9200

.PHONY: es-index-delete
es-index-delete: get-es-cert
	@echo "Delete existing index in Elasticseasrch"
	curl --cacert http_ca.crt -u elastic:elastic -XDELETE https://localhost:9200/himitsu_dogu?pretty=true

.PHONY: test-es-analyzer
test-es-analyzer: get-es-cert
	curl --cacert http_ca.crt -u elastic:elastic -X POST "https://localhost:9200/himitsu_dogu/_analyze?pretty" -H 'Content-Type: application/json' -d'{"analyzer": "custome_ja_analyzer","text":"ドラえもんのひみつ道具はどこでもドア以外にもたくさん存在する"}'

.PHONY: test-es-multimatch
test-es-multimatch: get-es-cert
	curl --cacert http_ca.crt -u elastic:elastic -X POST "https://localhost:9200/himitsu_dogu/_search?pretty" -H 'Content-Type: application/json' -d'{"query": {"multi_match" : {"query":"どこでもドア", "fields": [ "name", "description" ] }}}'

.PHONY: run-app
run-app: get-es-cert
	@echo "Running the web app for Doraemon himitsu dogu search"
	poetry run streamlit run doraemon_himitsu_dogu_search/app.py