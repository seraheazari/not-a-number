from pathlib import PurePath

import unicodedata


persian_to_latin_sentences = dict()
mapping_path = PurePath(__file__).with_name('sentences.csv')
with open(mapping_path) as f:
    for line in f:
        fa_en = line.split(',')
        persian_to_latin_sentences[fa_en[0]] = fa_en[1][:-1]


def latinize_sentence(persian_str):
    return persian_to_latin_sentences[persian_str]


def clean_persian_string(string):
    whitelist = {"Lu", "Ll", "Lo", "No", "Pe", "Ps", "Zs"}
    whited = [c for c in string if unicodedata.category(c) in whitelist]
    ya_replaced = ["ی" if c == "ي" else c for c in whited]
    return "".join(ya_replaced).strip()
