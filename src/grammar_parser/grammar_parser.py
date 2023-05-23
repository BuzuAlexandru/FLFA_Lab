class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def parse(tokens):
    try:
        ast = Node("Grammar")
        while tokens:
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
            else:
                raise Exception(f'Syntax error: expected VN, VT or PRODUCTION, found {current_token[0]}')
    except IndexError:
        raise Exception('Syntax error: ran out of tokens')

    return ast


def print_ast(node, indent=0):
    print('  ' * indent, end='')
    print(node.value)

    for child in node.children:
        print_ast(child, indent + 2)
