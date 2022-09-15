import os
import json
import numpy as np
from tabulate import tabulate


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


def to_bio_format(sentence, found):
    if not sentence or not found:
        return []
    n = sentence.count(' ') + 1
    tags = ['O'] * n
    found = [el for el in found if el.get('positions', [])]

    found.sort(key=lambda x: x['positions'][0])

    for el in found:
        for idx, pos in enumerate(el['positions']):
            if idx == 0:
                tags[pos] = f"B-{el['label']}"
            else:
                tags[pos] = f"I-{el['label']}"
    return {"sentence": sentence.split(), "tags": tags}


def compress_match_strings(sentence, query, sep: str = ' '):
    if not sentence or not query:
        return []
    clear_sentence = sentence.replace(sep, '').lower()
    spaces_dp = [0] * len(clear_sentence)
    query = query.replace(sep, '').lower()
    curr = 0
    dp_iter = 0
    for idx in range(len(sentence)):
        if sentence[idx] == sep:
            curr += 1
        else:
            spaces_dp[dp_iter] = curr
            dp_iter += 1

    # result = regex.search(f"({query})" + "{e<=3}", clear_sentence)
    start = clear_sentence.find(query)
    if start == -1:
        return []
    start = start
    end = start + len(query)
    results = list(set(spaces_dp[start:end]))
    results = list(sorted(results))

    return results


amazon_meta_all_beauty = os.path.join(
    os.path.abspath(''),
    '../data/nonnormalizedOffers_english.json'
)

n = 30 * 1000
offers = []
with open(amazon_meta_all_beauty, 'r') as f:
    i = 0
    for jsonObj in f:
        i += 1
        if i > n:
            break
        tmp = json.loads(jsonObj)
        offers.append(tmp)


def clean_el(el):
    for repl in ["@ru-ru", '@en-US', '@fr-CH', '@bg', '@lv', '@nl',
                 '@en', '@ja', '@vi', '@de',
                 '@it-IT', '@it']:
        el = el.replace(repl, '')
    el = el.replace('\n', '')
    el = el.replace('\t', '')
    if el[:2] == '["':
        el = el[2:]
    if el[-2:] == '"]':
        el = el[:-2]
    if el[:1] == '[':
        el = el[1:]
    if el[-1:] == ']':
        el = el[:-1]
    el = el.strip()
    return el


extracted_data = []
sentences = []
tags = []
counts = {}

props_count = {'schema.org_properties': {}, 'identifiers': {}}
props_example = {'schema.org_properties': {}, 'identifiers': {}}


def run_count(els, ke, pr):
    for p in els[ke]:
        for k in p.keys():
            pr[ke][k] = pr[ke].get(k, 0) + 1


def run_example(els, ke, pr):
    for p in els[ke]:
        for k in p.keys():
            pr[ke][k] = p[k]


keys = ['schema.org_properties', 'identifiers']
for idx, el in enumerate(offers):
    for k in keys:
        run_count(el, k, props_count)
        run_example(el, k, props_example)

print(props_count)
print(props_example)
upcs = 0

table = []
for k in keys:
    table.append([k, ""])
    els = []
    for ke, va in props_count[k].items():
        els.append([ke, va, props_example[k][ke]])
    els.sort(key=lambda x: x[1], reverse=True)
    for x in els:
        table.append(x)

result = tabulate(table, ['Attribute', 'Count', 'Example'], tablefmt='latex_longtable')
print(result)

a = 3

for idx, el in enumerate(offers):
    keys = set()
    for prop in el['schema.org_properties']:
        keys = keys | set(list(prop.keys()))
    edata = {}
    if 'schema.org_properties' in el and '/name' in keys:
        data = {}
        for d in el['schema.org_properties']:
            data = {**data, **d}

        edata['title'] = clean_el(data['/name'])
        if '/manufacturer' in data:
            edata['brand'] = data['/manufacturer']
        if '/brand' in data:
            edata['brand'] = data['/brand']

    ids = {}
    for d in el['identifiers']:
        ids = {**ids, **d}

    def insert_if(k, ed, idss):
        if k in idss:
            ed[k[1:]] = idss[k]

    for k in ['/sku',
              '/mpn',
              '/productID',
              '/gtin13',
              '/gtin12',
              '/gtin8',
              '/gtin14',
              '/identifier']:
        insert_if(k, edata, ids)
    # if '/sku' in ids:
    #     edata['sku'] = ids['/sku']
    # if '/mpn' in ids:
    #     edata['mpn'] = ids['/mpn']
    # if '/sku' in ids:
    #     edata['sku'] = ids['/sku']
    if '/productID' in ids:
        edata['pid'] = ids['/productID']
        if 'upc' in edata['pid']:
            upcs += 1
            splits = edata['pid'].split('upc')
            edata['sku'] = splits[0]
            edata['upc'] = splits[1]

    if 'title' in edata:
        counts['title'] = counts.get('title', 0) + 1
        for k in edata:
            edata[k] = clean_el(edata[k])
        found = []
        for k in edata:
            if k != 'title' and k in ['brand', 'mpn', 'sku', 'productID']:
                positions = compress_match_strings(edata['title'], edata[k], ' ') or compress_match_strings(
                    edata['title'].replace('-', ''), edata[k], ' ')
                if positions:
                    counts[k] = counts.get(k, 0) + 1
                label = k
                found.append({'positions': positions, 'label': label})
        if found and edata['title']:
            bio = to_bio_format(edata['title'], found)
            sentences.append(bio['sentence'])
            tags.append(bio['tags'])
            print(idx, edata, found)
            print(el)
            print('\n\n')

print(counts)

table = []
for k in counts:
    table.append([k, counts[k]])
table.sort(key=lambda x: x[1], reverse=True)

result = tabulate(table, ['Label', 'Count'], tablefmt='latex_longtable')
print(result)
print(f'upcs = {upcs}')

save_dataset(sentences, tags, os.path.join(os.path.dirname(__file__), "../ner_set"))

# print(idx, el['parent_schema.org_properties'][0])
