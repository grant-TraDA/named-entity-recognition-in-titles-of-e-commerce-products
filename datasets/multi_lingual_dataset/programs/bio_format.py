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


if __name__ == '__main__':
    bio = to_bio_format('LEGO Creator Winter Village Fire Station 10263 Ages 12 1166 pcs L',
                  [
                      {
                          "label": "BRAND",
                          "positions": [0]
                      },
                      {
                          "label": "SETNAME",
                          "positions": [2, 3, 4, 5]
                      },
                      {
                          "label": "SETNUMBER",
                          "positions": [6]
                      },
                      {
                          "label": "THEME",
                          "positions": [1]
                      }
                  ]
                  )
    print(bio)
