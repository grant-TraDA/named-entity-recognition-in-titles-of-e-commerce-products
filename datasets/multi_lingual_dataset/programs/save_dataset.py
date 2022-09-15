import os
import numpy as np


def save_dataset(sentences, tags, results_path):
    np.random.seed(1)
    array1 = np.array(sentences)
    array2 = np.array(tags)
    shuffler = np.random.permutation(len(array1))
    sentences = list(array1[shuffler])
    tags = list(array2[shuffler])

    output_count = len(sentences)

    parts = [
        {"label": "train", "start": 0.0, "end": 0.7},
        {"label": "test", "start": 0.7, "end": 0.85},
        {"label": "valid", "start": 0.85, "end": 1.0}
    ]

    for part in parts:
        part_path = os.path.join(results_path, f"{part['label']}.txt")
        start = int(output_count * part['start'])
        end = int(output_count * part['end'])

        result_file = open(part_path, 'w+')

        for idx in range(start, end):
            data_sentence = sentences[idx]
            data_tags = tags[idx]
            for token, tag in zip(data_sentence, data_tags):
                result_file.write(f'{token}\t{tag}\n')
            result_file.write('\n')
        result_file.close()
