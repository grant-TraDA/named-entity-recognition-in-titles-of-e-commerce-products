from keyvalues_data import KEYVALUES_TOYS
from tabulate import tabulate

KEYVALUES_TOYS['de'].sort(key=lambda x: x['label'])


def generate_table(keyvalues):
    keyvalues.sort(key=lambda x: x['label'])
    table = []

    def trim(s, n=15):
        return f"{s[:n]}..." if len(s) > n else s

    for x in keyvalues:
        if 'example' in x:
            example = trim(x['example'])
            translation = trim(x['translation'].replace(':', ''), n=35)
            table.append([x['label'], translation, example])

    result = tabulate(table, ['Label', 'Attribute', 'Example'], tablefmt='latex_longtable')
    return result
