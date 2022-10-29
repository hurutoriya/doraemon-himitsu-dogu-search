import json

import numpy as np
import sentents_bert

from data import HIMITSU_DOGU_DATA_PATH, MODEL_NAME, SENTENTS_VECTOR_DATA_PATH


def main():
    model = sentents_bert.SentenceBertJapanese(MODEL_NAME)

    with open(HIMITSU_DOGU_DATA_PATH, "r") as f:
        himitsu_dogus = json.load(f)

    himitsu_docs_descriptions = [himitsu_dogu["description"] for himitsu_dogu in himitsu_dogus]
    print("Start BERT encode")
    sentence_embeddings = model.encode(himitsu_docs_descriptions, batch_size=32)
    print("End BERT encode")

    print("Start serialization as numpy file")
    np.save(SENTENTS_VECTOR_DATA_PATH, sentence_embeddings.cpu().detach().numpy())
    print("End serialization")


if __name__ == "__main__":
    main()
