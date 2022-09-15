import random


def full_data_extraction(description, keyvalues):
    results = {}

    positions = []
    for idx, kv in enumerate(keyvalues):
        pos = 0
        while True:
            pos = description.find(kv['translation'], pos)
            if pos == -1:
                break
            positions.append([pos, idx])
            pos += len(kv['translation'])

    positions.sort(key=lambda x: x[0])

    n_pos = len(positions)
    for idx in range(n_pos):
        start = positions[idx][0]+len(keyvalues[positions[idx][1]]['translation'])
        if idx < n_pos-1:
            end = positions[idx+1][0]
        else:
            end = len(description)
        extracted_element = description[start:end].strip()

        if extracted_element and ':' not in extracted_element:
            keyvalues[positions[idx][1]]['example'] = extracted_element
            results[keyvalues[positions[idx][1]]['label']] = extracted_element

    return results

