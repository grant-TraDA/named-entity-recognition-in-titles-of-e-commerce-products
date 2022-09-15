import regex


def compress_match_strings(sentence, query):
    if not sentence or not query:
        return []
    clear_sentence = sentence.replace(' ', '').lower()
    spaces_dp = [0] * len(clear_sentence)
    query = query.replace(' ', '').lower()
    curr = 0
    dp_iter = 0
    for idx in range(len(sentence)):
        if sentence[idx] == ' ':
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


if __name__ == '__main__':
    matches = compress_match_strings(
        'Galaxy Note 20 Ultra Verizon Unlocked 128GB Black Pristine condition',
        'Galaxy Note20 Ultra'
    )
    print(matches)
