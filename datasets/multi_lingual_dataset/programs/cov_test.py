from compress_string_matching import compress_match_strings


def coverage_test(counts, language, title, extracted_data):
    if language not in counts:
        counts[language] = {}
    for k in extracted_data:
        matches = compress_match_strings(title, str(extracted_data[k]))
        if matches:
            if k not in counts[language]:
                counts[language][k] = 1
            else:
                counts[language][k] += 1
