import os
import pandas as pd
import json
import re
from keyvalues_data import KEYVALUES_TOYS
from description_extraction import full_data_extraction
from compress_string_matching import compress_match_strings
from bio_format import to_bio_format
from save_dataset import save_dataset
from tabulate import tabulate
from table_generator import generate_table
from cov_test import coverage_test


DE_DATASET_NON_NORMALIZED_PATH_test = os.path.join(
    os.path.abspath(''),
    '../final_datasets/multi_class_test_set_toy.csv'
)
DE_DATASET_NON_NORMALIZED_PATH_train = os.path.join(
    os.path.abspath(''),
    '../final_datasets/multi_class_train_set_toy.csv'
)

products_train = pd.read_csv(DE_DATASET_NON_NORMALIZED_PATH_train, index_col=False)
products_test = pd.read_csv(DE_DATASET_NON_NORMALIZED_PATH_test, index_col=False)

products = pd.concat([products_train, products_test])

products['description'] = products['description'].astype(str)

languages = list(products['lang'].unique())
languages = ['en', 'de', 'es', 'fr']

sentences = []
tags = []

counts = {}
ov_len = 0



matches_count = {}

sentences = []
tags = []

for language in languages:

    lang_subset = products[products['lang'] == language]
    keyvalues = KEYVALUES_TOYS[language]


    count = 0

    for product in lang_subset.iterrows():
        extracted_data = full_data_extraction(product[1]['description'], keyvalues)

        brand = str(product[1]['subcategory'])
        set_name = str(extracted_data.get('set_name', None))
        set_number = str(extracted_data.get('set_number', None))
        theme = str(extracted_data.get('theme', None))
        ov_len += 1
        matches_brand = compress_match_strings(product[1]['title'], brand)
        matches_set_name = compress_match_strings(product[1]['title'], set_name)
        matches_set_number = compress_match_strings(product[1]['title'], set_number)
        matches_theme = compress_match_strings(product[1]['title'], theme)
        coverage_test(counts, language, product[1]['title'], extracted_data)

        if True or (matches_brand and matches_set_name and matches_set_number and matches_theme):
            found = [
                {
                    "label": "BRAND",
                    "positions": matches_brand
                },
                {
                    "label": "SETNAME",
                    "positions": matches_set_name
                },
                {
                    "label": "SETNUMBER",
                    "positions": matches_set_number
                },
                {
                    "label": "THEME",
                    "positions": matches_theme
                }
            ]

            bio = to_bio_format(product[1]['title'], found)
            sentences.append(bio['sentence'])
            tags.append(bio['tags'])
            count += 1

    table = generate_table(keyvalues)
    print(f'{table}\n\n\n')

save_dataset(sentences, tags, os.path.join(os.path.dirname(__file__), f"../ner_set/toys/all"))

# print(ov_len)
# print(counts)


# table = [[] for x in range(n)]
#
# for lang in languages + ['full']:
#     for el in range(n):
#         table[el].append(table_counts[lang][el][0])
#     for el in range(n):
#         table[el].append(table_counts[lang][el][1])


table_counts = {}
for lang in languages:
    table_counts[lang] = [[k, counts[lang][k]] for k in counts[lang]]
    table_counts[lang].sort(key=lambda x: x[1], reverse=True)

full_counts = {}
for lang in languages:
    for d in counts[lang]:
        full_counts[d] = full_counts.get(d, 0) + counts[lang][d]
table_counts['full'] = [[k, full_counts[k]] for k in full_counts]
table_counts['full'].sort(key=lambda x: x[1], reverse=True)


n = 5
table = []

for lang in languages + ['full']:
    tmp = [lang]
    for el in range(n):
        tmp.append(table_counts[lang][el][0])
    table.append(tmp)

    tmp = [""]
    for el in range(n):
        tmp.append(table_counts[lang][el][1])
    table.append(tmp)

table = tabulate(table, tablefmt='latex_longtable')
print("\n\n###\n\n")
print(table)
print("\n\n###\n\n")

# print(table_counts)


