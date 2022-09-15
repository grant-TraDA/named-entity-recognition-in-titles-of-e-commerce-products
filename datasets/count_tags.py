from tabulate import tabulate


def count_tags(path, tags):

    counts = {"test.txt": {}, "train.txt": {}, "valid.txt": {}}

    files_list = ["train.txt", "valid.txt", "test.txt"]

    for s in files_list:
        with open(f'{path}/{s}', 'r') as f:
            for line in f:
                if line == '\n':
                    counts[s]['sentences'] = counts[s].get('sentences', 0) + 1
                for tag in tags:
                    k = f'B-{tag}'
                    if k in line:
                        counts[s][k] = counts[s].get(k, 0) + 1
                    k = f'I-{tag}'
                    if k in line:
                        counts[s][k] = counts[s].get(k, 0) + 1

    table = []
    for t in tags:
        for pre in ['B', 'I']:
            curr = [f'{pre}-{t}']
            for k in files_list:
                curr.append(counts[k].get(f'{pre}-{t}', 0))
            curr.append(sum(curr[1:]))
            table.append(curr)
        curr = [t]
        for k in files_list:
            curr.append(counts[k].get(f'B-{t}', 0) + counts[k].get(f'I-{t}', 0))

        curr.append(sum(curr[1:]))
        table.append(curr)
    curr = ['SENTENCES']
    for k in files_list:
        curr.append(counts[k]['sentences'])
    curr.append(sum(curr[1:]))
    table.append(curr)

    return table


table = count_tags("multi_lingual_dataset/ner_set/toys/all",
                   ["BRAND", "SETNAME", "SETNUMBER", "THEME"])
table = tabulate(table, ['Tag', 'Train', 'Valid', 'Test', 'Combined'], tablefmt='latex_longtable')
print("\n\n###\n\n")
print(table)
print("\n\n###\n\n")
