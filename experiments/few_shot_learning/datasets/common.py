import datasets
from tqdm import tqdm
import os

DESCRIPTION = """CoNLL format dataset"""


def generate_examples(filepath, tags_dict):
    num_lines = sum(1 for _ in open(filepath))
    id = 0

    with open(filepath, "r") as f:
        tokens, ner_tags = [], []
        for line in tqdm(f, total=num_lines):
            line = line.strip().split()

            if line:
                assert len(line) == 2
                token, ner_tag = line

                if token == "-DOCSTART-":
                    continue

                tokens.append(token)
                ner_tags.append(tags_dict[ner_tag])

            elif tokens:
                # organize a record to be written into json
                record = {
                    "id": str(id),
                    "tokens": tokens,
                    "ner_tags": ner_tags,
                }
                tokens, ner_tags = [], []
                id += 1
                yield record["id"], record

        # take the last sentence
        if tokens:
            record = {
                "id": str(id),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
            yield record["id"], record


def generate_info(ner_tags):
    return datasets.DatasetInfo(
        description=DESCRIPTION,
        features=datasets.Features(
            {
                "id": datasets.Value("string"),
                "tokens": datasets.features.Sequence(datasets.Value("string")),
                "ner_tags": datasets.features.Sequence(
                    datasets.features.ClassLabel(
                        names=list(ner_tags.keys())
                    )
                ),
            }
        ),
        supervised_keys=None,
    )


def get_splits(type, lang):
    path = f"ner_set/{type}/{lang}"
    return [
        datasets.SplitGenerator(
            name=datasets.Split.TRAIN,
            gen_kwargs={
                "filepath": os.path.join(os.path.dirname(__file__), f"{path}/train.txt")
            },
        ),
        datasets.SplitGenerator(
            name=datasets.Split.TEST,
            gen_kwargs={
                "filepath": os.path.join(os.path.dirname(__file__), f"{path}/test.txt")
            },
        ),
        datasets.SplitGenerator(
            name=datasets.Split.VALIDATION,
            gen_kwargs={
                "filepath": os.path.join(os.path.dirname(__file__), f"{path}/valid.txt")
            },
        ),
    ]


PHONE_TAGS = {
    "O": 0,
    "B-BRAND": 1,
    "I-BRAND": 2,
    "B-MEMORY": 3,
    "I-MEMORY": 4,
    "B-MODEL": 5,
    "I-MODEL": 6,
    "B-COLOR": 7,
    "I-COLOR": 8,
}

TOY_TAGS = {
    "O": 0,
    "B-BRAND": 1,
    "I-BRAND": 2,
    "B-SETNUMBER": 3,
    "I-SETNUMBER": 4,
    "B-SETNAME": 5,
    "I-SETNAME": 6,
    "B-THEME": 7,
    "I-THEME": 8,
}
