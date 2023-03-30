# Laboratory work nr.3
# Lexer & Scanner
### University: Technical University of Moldova
### Course: Formal Languages & Finite Automata
### Author: Alexandru Buzu, FAF 212 (variant 4)

---

## Objectives:
1. Understand what lexical analysis is. 
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.
## Theory
A lexer, also known as a lexical analyzer or scanner, is a program 
or a module that performs lexical analysis on a stream of input 
characters to produce a sequence of tokens.

The main functionality of a lexer is to break down the input string 
into smaller pieces called tokens, which are then passed to a parser 
for further processing. Tokens represent meaningful units of the 
input, such as identifiers, keywords, numbers, and punctuation symbols, 
and they are usually defined by a regular grammar or a set of regular 
expressions.

## Implementation description
For the purpose fo this laboratory work, I chose to make a lexer for
the definition of a regular grammar from Lab 1, that accepts terminal and
non-terminal symbols in the form of letters:
```text
VN={S, L, D},
VT={a, b, c, d, e, f, j},
P={
    S → aS
    S → bS
    S → cD
    S → dL
    S → e
    L → eL
    L → fL
    L → jD
    L → e
    D → eD
    D → d
}
```
Beside some characters like brackets, operators or commas, the base 
components of a grammar are the non-terminal symbols, 
terminal symbols and production rules. As such, using the `re`
module in Python I made regular expressions for all elements that
make up the text above, which are then used to identify tokens later on.

Some notations that I use are: space followed by a star `_*`, which means
zero or more occurrences of a space between certain characters; 
square brackets are used to show sets of characters `[a-z]`; and the
separator `|` used to combine multiple regular expressions into one.
```python
    VN = r'VN *='
    VT = r'VT *='
    PRODUCTION = r'P *='
    RIGHTSIDE = r'→ *[a-zA-Z]+|→ *ε'
    NONTERMINAL = r'[A-Z],|[A-Z]'
    TERMINAL = r'[a-z],|[a-z]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    SKIP = r',|\n|\t| '
    OPERATOR = r'=|→'
```
To facilitate the later use of the regular expressions, I used the `join()`
method to combine them into a common unique regular expression.
```python
    regular_expression = '|'.join([VN, VT, PRODUCTION, RIGHTSIDE, NONTERMINAL, 
                                TERMINAL, LBRACE, RBRACE, SKIP, OPERATOR])
```
After that the `tokens` list is initiated, as well as the `error_test`
string, used to identify if the input text has any characters that do
not correspond to the regular expressions.

Next, the `finditer()` function is used together with the regular
expression and the input text. This function finds all the 
non-overlapping matches of the regex in the text, and creates an 
iterable list of `match` objects. The value of the `match` object can
be accessed using the `group()` method, which returns the string that
was found to be matching the regex.
```python
    tokens = []
    error_test = ''
    for token in re.finditer(regular_expression, code):
        value = token.group()
        error_test += value
```
Next, each match found is run through a series of `if` statements that
are used to determine the type of token it represents. Whitespaces, tab
characters, newline characters and commas are omitted. And for some values
the whitespaces need to be removed manually as well as separating certain
characters that are used in the regular expressions to identify tokens.
The token names and values are then appended to the token list.
```python
        if re.match(SKIP, value):
            continue
        elif re.match(VN, value):
            tokens.append(('VN',))
            tokens.append(('OPERATOR', '='))
        elif re.match(VT, value):
            tokens.append(('VT',))
            tokens.append(('OPERATOR', '='))
        elif re.match(PRODUCTION, value):
            tokens.append(('PRODUCTION',))
            tokens.append(('OPERATOR', '='))
        elif re.match(RIGHTSIDE, value):
            tokens.append(('OPERATOR', '→'))
            tokens.append(('RIGHTSIDE', value.replace('→', '').replace(' ', '')))
        elif re.match(NONTERMINAL, value):
            tokens.append(('NONTERMINAL', value.replace(',', '')))
        elif re.match(TERMINAL, value):
            tokens.append(('TERMINAL', value.replace(',', '')))
        elif re.match(LBRACE, value):
            tokens.append(('LBRACE',))
        elif re.match(RBRACE, value):
            tokens.append(('RBRACE',))
        elif re.match(OPERATOR, value):
            tokens.append(('OPERATOR', value))
```
Finally, the `error_test` variable, that is a concatenation of all found
values, is compared with the input text. If they are equal, the token list
is returned, otherwise the text contains a character that was not 
specified in the regex and a error is raised.
```python
    if error_test == code:
        return tokens
    else:
        raise ValueError('Faulty text input')
```


## Results
Testing the lexer on the Lab 1, variant 4 grammar:
```python
text = '''
VN={S, L, D},
VT={a, b, c, d, e, f, j},
P={
    S → aS
    S → bS
    S → cD
    S → dL
    S → e
    L → eL
    L → fL
    L → jD
    L → e
    D → eD
    D → d
}
'''
for token in grammar_lexer(text):
    print(token)
```
Output:
```
('VN',)
('OPERATOR', '=')
('LBRACE',)
('NONTERMINAL', 'S')
('NONTERMINAL', 'L')
('NONTERMINAL', 'D')
('RBRACE',)
('VT',)
('OPERATOR', '=')
('LBRACE',)
('TERMINAL', 'a')
('TERMINAL', 'b')
('TERMINAL', 'c')
('TERMINAL', 'd')
('TERMINAL', 'e')
('TERMINAL', 'f')
('TERMINAL', 'j')
('RBRACE',)
('PRODUCTION',)
('OPERATOR', '=')
('LBRACE',)
('NONTERMINAL', 'S')
('OPERATOR', '→')
('RIGHTSIDE', 'aS')
('NONTERMINAL', 'S')
('OPERATOR', '→')
('RIGHTSIDE', 'bS')
('NONTERMINAL', 'S')
('OPERATOR', '→')
('RIGHTSIDE', 'cD')
('NONTERMINAL', 'S')
('OPERATOR', '→')
('RIGHTSIDE', 'dL')
('NONTERMINAL', 'S')
('OPERATOR', '→')
('RIGHTSIDE', 'e')
('NONTERMINAL', 'L')
('OPERATOR', '→')
('RIGHTSIDE', 'eL')
('NONTERMINAL', 'L')
('OPERATOR', '→')
('RIGHTSIDE', 'fL')
('NONTERMINAL', 'L')
('OPERATOR', '→')
('RIGHTSIDE', 'jD')
('NONTERMINAL', 'L')
('OPERATOR', '→')
('RIGHTSIDE', 'e')
('NONTERMINAL', 'D')
('OPERATOR', '→')
('RIGHTSIDE', 'eD')
('NONTERMINAL', 'D')
('OPERATOR', '→')
('RIGHTSIDE', 'd')
('RBRACE',)
```
Text input with a `;` that is not included in the regular expression:
```python
text = '''
VN={S, L, D};
'''
for i in grammar_lexer(text):
    print(i)
```
Output:
```text
line 52, in grammar_lexer
    raise ValueError('Faulty text input')
ValueError: Faulty text input
```

## Conclusions
During this laboratory work I have learned the process of lexical analysis
and the inner workings of a lexer. Beside that, I have also implemented a
lexer that works based on regular expressions using the `re` python module.
Overall, it was a good learning experience in terms of studying how 
the first steps of creating a programming languages are. And even though
my lexer works just fine for the proposed grammar definition, I am
confident there is much room for improvement in its implementation.