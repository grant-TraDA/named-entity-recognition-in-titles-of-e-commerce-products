import os
import pandas as pd
import json
import re
from keyvalues_data import KEYVALUES_TOYS
from description_extraction import full_data_extraction
from compress_string_matching import compress_match_strings
from bio_format import to_bio_format
from save_dataset import save_dataset
from matplotlib import pyplot as plt


DE_DATASET_NON_NORMALIZED_PATH_test = os.path.join(
    os.path.abspath(''),
    '../data/multi_class_test_set_phone.csv'
)
DE_DATASET_NON_NORMALIZED_PATH_train = os.path.join(
    os.path.abspath(''),
    '../data/multi_class_train_set_phone.csv'
)

products_train = pd.read_csv(DE_DATASET_NON_NORMALIZED_PATH_train, index_col=False)
products_test = pd.read_csv(DE_DATASET_NON_NORMALIZED_PATH_test, index_col=False)

products = pd.concat([products_train, products_test])

products['description'] = products['description'].astype(str)


def title_analysis(data, counter, label):
    title_counts = {}
    for idx, product in data.iterrows():
        title_count = counter(product)
        title_counts[title_count] = title_counts.get(title_count, 0) + 1

    plt.bar(title_counts.keys(),
            title_counts.values(),
            color='g')

    plt.title(f'Distribution of title lengths, phone dataset')
    plt.xlabel('Length')
    plt.ylabel(f'{label} count')
    plt.show()


title_analysis(products, lambda product: product['title'].count(' ') + 1, 'Word')
title_analysis(products, lambda product: len(product['title']), 'Character')
