import os
import pandas as pd
from keyvalues_data import KEYVALUES_PHONES
from description_extraction import full_data_extraction
from compress_string_matching import compress_match_strings
from bio_format import to_bio_format
from save_dataset import save_dataset
from tabulate import tabulate
from table_generator import generate_table
from cov_test import coverage_test

DE_DATASET_NON_NORMALIZED_PATH_test = os.path.join(
    os.path.abspath(''),
    '../data/multi_class_test_set_phone.csv'
)
DE_DATASET_NON_NORMALIZED_PATH_train = os.path.join(
    os.path.abspath(''),
    '../data/multi_class_train_set_phone.csv'
)

GENERATE_FILE_SUMMARY_TABLE = True
GENERATE_KEYVALUES_TABLE = True
GENERATE_ATTRIBUTES_IN_LANGUAGE_SUMMARY_TABLE = True

products_train = pd.read_csv(DE_DATASET_NON_NORMALIZED_PATH_train, index_col=False)
products_test = pd.read_csv(DE_DATASET_NON_NORMALIZED_PATH_test, index_col=False)

products = pd.concat([products_train, products_test])

if GENERATE_FILE_SUMMARY_TABLE:
    brands = set(products_test['lang'].unique()) | set(products_test['lang'].unique())
    data = []
    for brand in brands:
        if not brand:
            continue
        tmp = {'brand': brand}
        data.append(tmp)
        tmp['train'] = sum(products_train['lang'] == brand)
        tmp['test'] = sum(products_test['lang'] == brand)

    data.sort(key=lambda x: x['train'] + x['test'], reverse=True)
    table = []
    for x in data:
        if x['train'] + x['test'] > 0:
            table.append([x['brand'].capitalize(), x['train'], x['test'], x['train'] + x['test']])

    result = tabulate(table, ['Language', 'Train', 'Test', 'Total'], tablefmt='latex_longtable')
    print(result)

products['description'] = products['description'].astype(str)

languages = list(products['lang'].unique())
languages = ['en', 'de', 'fr', 'es']

counts = {}

sentences_all = []
tags_all = []

for language in languages:
    lang_subset = products[products['lang'] == language]
    keyvalues = KEYVALUES_PHONES[language]

    sentences = []
    tags = []

    count = 0
    for product in lang_subset.iterrows():
        extracted_data = full_data_extraction(product[1]['description'], keyvalues)

        brand = str(product[1]['subcategory'])
        model = str(extracted_data.get('model', None))
        if model and brand:
            model = model.lower().replace(brand, '')
        color = extracted_data.get('color', None)
        storage = extracted_data.get('memory', None)

        matches_brand = compress_match_strings(product[1]['title'], brand)
        matches_model = compress_match_strings(product[1]['title'], model)
        matches_color = compress_match_strings(product[1]['title'], color)
        matches_storage = compress_match_strings(product[1]['title'], storage)

        coverage_test(counts, language, product[1]['title'], extracted_data)

        found = [
            {
                "label": "BRAND",
                "positions": matches_brand
            },
            {
                "label": "MODEL",
                "positions": matches_model
            },
            {
                "label": "COLOR",
                "positions": matches_color
            },
            {
                "label": "MEMORY",
                "positions": matches_storage
            }
        ]

        bio = to_bio_format(product[1]['title'], found)

        sentences.append(bio['sentence'])
        tags.append(bio['tags'])

        sentences_all.append(bio['sentence'])
        tags_all.append(bio['tags'])

        count += 1

    save_dataset(sentences, tags, os.path.join(os.path.dirname(__file__), f"../ner_set/phones/{language}"))

    if GENERATE_KEYVALUES_TABLE:
        table = generate_table(keyvalues)
        print(table)

save_dataset(sentences_all, tags_all, os.path.join(os.path.dirname(__file__), f"../ner_set/phones/all"))

if GENERATE_ATTRIBUTES_IN_LANGUAGE_SUMMARY_TABLE:
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
