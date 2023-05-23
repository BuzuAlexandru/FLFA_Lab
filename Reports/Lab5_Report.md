# Laboratory work nr.5
# Parser & Building an Abstract Syntax Tree
### University: Technical University of Moldova
### Course: Formal Languages & Finite Automata
### Author: Alexandru Buzu, FAF 212 (variant 4)

---

## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed.
2. Get familiar with the concept of AST.
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.
## Implementation description
In the previous lab, I already used regular expressions to identify the type of tokens.
```python
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
```
And the tokens were already generated as enum style, with token name and
value in a tuple.
```
('NONTERMINAL', 'S')
('OPERATOR', '→')
('RIGHTSIDE', 'aS')
('NONTERMINAL', 'S')
('OPERATOR', '→')
('RIGHTSIDE', 'bS')
```
For the AST I implemented the Node class that allows to create the tree data structure.
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
```
Next I defined a parser function that takes each token one by one and
checks whether it precedes the correct tokens. When an illegal token
is found, an error is raised. 
The AST that is created while parsing has three children from the root:
nonterminal symbols, terminal symbols and production rules, in no specific order.

If a `VN` token is found, a `VN` child is added to the AST, and subsequent
`NONTERMINAL` tokens values are added as children to `VN`. 
```python
ast = Node("Grammar")
while len(tokens):
   current_token = tokens.pop(0)
   if current_token[0] == 'VN':
       vn = Node(current_token[1])
       if tokens.pop(0)[1] == '=' and tokens.pop(0)[0] == 'LBRACE':
           while True:
               nterm = tokens.pop(0)
               if nterm[0] == 'RBRACE':
                   break
               elif nterm[0] == 'NONTERMINAL':
                   vn.add_child(Node(nterm[1]))
               else:
                   raise Exception('Syntax error at nonterminal symbols')
       else:
           raise Exception('Syntax error at nonterminal symbols')
       ast.add_child(vn)
```
For the terminal symbols, the process is the same as for the nonterminal ones.
```python
elif current_token[0] == 'VT':
    vt = Node(current_token[1])
    if tokens.pop(0)[1] == '=' and tokens.pop(0)[0] == 'LBRACE':
        while True:
            term = tokens.pop(0)
            if term[0] == 'RBRACE':
                break
            elif term[0] == 'TERMINAL':
                vt.add_child(Node(term[1]))
            else:
                raise Exception('Syntax error at terminal symbols')
    else:
        raise Exception('Syntax error at terminal symbols')
    ast.add_child(vt)
```
For the `PRODUCTION` child, for each production rule, a new `RULE` child is added
to `PRODUCTION`, and each `RULE` has two children that represent the left
side and the right side of the production rule.
```text
PROD
     RULE
         LEFT
             S
         RIGHT
             aS
```
```python
elif current_token[0] == 'PRODUCTION':
    prod = Node('PROD')
    if tokens.pop(0)[1] == '=' and tokens.pop(0)[0] == 'LBRACE':
        while True:
            lside = tokens.pop(0)
            if lside[0] == 'RBRACE':
                break
            op = tokens.pop(0)
            rside = tokens.pop(0)

            if lside[0] == 'NONTERMINAL' and op[1] == '→' and rside[0] == 'RIGHTSIDE':
                rule = Node('RULE')
                aux = Node('LEFT')
                aux.add_child(Node(lside[1]))
                rule.add_child(aux)
                aux = Node('RIGHT')
                aux.add_child(Node(rside[1]))
                rule.add_child(aux)
                prod.add_child(rule)
            else:
                raise Exception('Syntax error at production rule')

    else:
        raise Exception('Syntax error at production')
    ast.add_child(prod)
```
Some more conditions set to raise syntax errors.
```python
      else:
          raise Exception(f'Syntax error: expected VN, VT or PRODUCTION, found {current_token[0]}')
except IndexError:
  raise Exception('Syntax error: ran out of tokens')

return ast
```
Tree printing function that prints children of the tree with increasing 
indents as the depth of the node is bigger.
```python
def print_ast(node, indent=0):
    print('  ' * indent, end='')
    print(node.value)

    for child in node.children:
        print_ast(child, indent + 2)
```
## Results
Testing on example grammar.
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

tokens = grammar_lexer(text)
ast = parse(tokens)
print_ast(ast)
```
Output:
```text
Grammar
    VN
        S
        L
        D
    VT
        a
        b
        c
        d
        e
        f
        j
    PROD
        RULE
            LEFT
                S
            RIGHT
                aS
        RULE
            LEFT
                S
            RIGHT
                bS
        RULE
            LEFT
                S
            RIGHT
                cD
        RULE
            LEFT
                S
            RIGHT
                dL
        RULE
            LEFT
                S
            RIGHT
                e
        RULE
            LEFT
                L
            RIGHT
                eL
        RULE
            LEFT
                L
            RIGHT
                fL
        RULE
            LEFT
                L
            RIGHT
                jD
        RULE
            LEFT
                L
            RIGHT
                e
        RULE
            LEFT
                D
            RIGHT
                eD
        RULE
            LEFT
                D
            RIGHT
                d
```
Checking for missing brace.
```python
text = '''
VN={S},
VT={a,
P={
    S → aS
}
'''
```
Output:
```text
Exception: Syntax error at terminal symbols
```
## Conclusions
During this laboratory work I have learned about parsing and abstract
syntax trees. Implementing these concepts was quite intuitive as I picked
something that is not too complex to parse, as such it did not take much time
to figure out.