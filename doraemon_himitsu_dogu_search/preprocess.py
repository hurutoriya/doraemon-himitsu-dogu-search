import dataclasses
import json
from dataclasses import dataclass

from data import HIMITSU_DOGU_DATA_PATH, HIMITSU_DOGU_RAW_DATA_PATH


@dataclass
class HimitsuDogu:
    """Class for structured Himitsu Dogu."""

    id: str
    name: str
    yomi: str
    description: str


# NOTE: https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses/51286749#51286749
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def main():
    """
    make structured data as json file from raw text file.
    """

    # NOTE: Number of one Himiatsu dogu lines
    HIMITSU_DOGU_LINE_NUM = 3

    with open(HIMITSU_DOGU_RAW_DATA_PATH, encoding="utf-8") as f:
        raw_data = f.readlines()
    himitsu_dogs = []
    doc_id = 1
    for idx in range(0, len(raw_data), HIMITSU_DOGU_LINE_NUM):
        himitsu_dogs.append(
            HimitsuDogu(
                id=doc_id,
                name=raw_data[idx].rstrip(),
                yomi=raw_data[idx + 1].rstrip(),
                description=raw_data[idx + 2].rstrip(),
            )
        )
        doc_id += 1
    # NOTE: https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
    with open(HIMITSU_DOGU_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(
            himitsu_dogs, f, ensure_ascii=False, indent=4, cls=EnhancedJSONEncoder
        )


if __name__ == "__main__":
    main()
