# Doraemon Himitsu Dogu Natural Language Search

Python based Doraemon Himitsu Dogu Natural Language Search based on Elasticsearch approximate nearest neighbor(ANN) feature.

Japanese: Elasticsearch の近似近傍探索機能を使ったドラえもんのひみつ道具自然言語検索エンジン

![](./docs/demo_v1.gif)

## Key technology

- HuggingFace
  - [sonoisa/sentence-bert-base-ja-mean-tokens-v2](https://huggingface.co/sonoisa/sentence-bert-base-ja-mean-tokens-v2)
- Elasticsearch
- Streamlit

## Dataset

I made a Himitdu Dogu dataset based on this site.
[ひみつ道具カタログ](https://www.tv-asahi.co.jp/doraemon/tool/a.html)

## Indexing phase

```mermaid
graph LR;
text-->|json形式に構造化|json
json-->|説明文|HuggingFace
json-->Elasticsaerch
HuggingFace-->|特徴ベクトル化|Elasticsaerch
```

## Search phase

```mermaid
graph LR;
Query-->|強くなる|id["HuggingFace(encoder)"]
subgraph Streamlit
    id["HuggingFace(encoder)"]
end
subgraph Elasticsearch
    ANN
end
id["HuggingFace(encoder)"]-->|"[1.2, ... 0.3]"|ANN
```
