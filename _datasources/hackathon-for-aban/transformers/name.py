from pathlib import PurePath

persian_to_latin_names = dict()
mapping_path = PurePath(__file__).with_name('names.csv')
with open(mapping_path) as f:
    for line in f:
        fa_en = line.split(',')
        persian_to_latin_names[fa_en[0]] = fa_en[1][:-1]


class Join(Exception):
    pass


def latinize_name(persian_str):
    translated = []
    tokens = persian_str.split(' ')
    n_tokens = len(tokens)
    prefix = ''
    parenthesize = False
    joining_postfixes = set(['فر', 'زاده'])
    for i, token in enumerate(tokens):
        if token[0] == '(':
            token = token[1:]
            parenthesize = True
        if token[-1] == ')':
            token = token[:-1]
            parenthesize = True
        try:
            if prefix:
                token = f"{prefix}{token}"
            if i + 1 < n_tokens and tokens[i+1] in joining_postfixes:
                raise Join
            latin = persian_to_latin_names[token]
            if parenthesize:
                latin = f"({latin})"
                parenthesize = False
            translated.append(latin)
            prefix = ''
        except (KeyError, Join) as e:
            if i + 1 < n_tokens:
                prefix = f"{token} "
            else:
                raise e
    return ' '.join(translated)
