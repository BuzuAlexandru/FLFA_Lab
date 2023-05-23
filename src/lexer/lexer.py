import re


def grammar_lexer(code):
    VN = r'VN *= *\{'
    VT = r'VT *= *\{'
    PRODUCTION = r'P *= *\{'
    RIGHTSIDE = r'→ *[a-zA-Z]+|→ *ε'
    NONTERMINAL = r'[A-Z],|[A-Z]'
    TERMINAL = r'[a-z],|[a-z]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    SKIP = r',|\n|\t| '
    OPERATOR = r'=|→'

    regular_expression = '|'.join([VN, VT, PRODUCTION, RIGHTSIDE, NONTERMINAL,
                                   TERMINAL, LBRACE, RBRACE, SKIP, OPERATOR])

    tokens = []
    error_test = ''
    for token in re.finditer(regular_expression, code):
        value = token.group()
        error_test += value
        if re.match(SKIP, value):
            continue
        elif re.match(VN, value):
            tokens.append(('VN', 'VN'))
            tokens.append(('OPERATOR', '='))
            tokens.append(('LBRACE', '{'))
        elif re.match(VT, value):
            tokens.append(('VT', 'VT'))
            tokens.append(('OPERATOR', '='))
            tokens.append(('LBRACE', '{'))
        elif re.match(PRODUCTION, value):
            tokens.append(('PRODUCTION', 'P'))
            tokens.append(('OPERATOR', '='))
            tokens.append(('LBRACE', '{'))
        elif re.match(RIGHTSIDE, value):
            tokens.append(('OPERATOR', '→'))
            tokens.append(('RIGHTSIDE', value.replace('→', '').replace(' ', '')))
        elif re.match(NONTERMINAL, value):
            tokens.append(('NONTERMINAL', value.replace(',', '')))
        elif re.match(TERMINAL, value):
            tokens.append(('TERMINAL', value.replace(',', '')))
        elif re.match(LBRACE, value):
            tokens.append(('LBRACE', '{'))
        elif re.match(RBRACE, value):
            tokens.append(('RBRACE', '}'))
        elif re.match(OPERATOR, value):
            tokens.append(('OPERATOR', value))

    if error_test == code:
        return tokens
    else:
        raise ValueError('Lexical error: Faulty text input')
