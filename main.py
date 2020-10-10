import sys

import ply.lex as lex

import ply.yacc as yacc

tokens = [
    'ID', 'DEF', 'TAIL', 'AND', 'OR', 'LBR', 'RBR'
]

t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_DEF = r':-'
t_TAIL = r'\.'
t_AND = r','
t_OR = r';'
t_LBR = r'\('
t_RBR = r'\)'

t_ignore = ' \t\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_def(p):
    '''def : atom TAIL
           | atom DEF or TAIL'''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = f'DEF({p[1]}), ({p[3]})'


def p_id(p):
    'id : ID'
    p[0] = p[1]


def p_subsubatom(p):
    '''subsubatom : id
                  | id subatom
                  | LBR subsubatom RBR'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = f'{p[1]} {p[2]}'
    elif len(p) == 4:
        p[0] = f'({p[2]})'


def p_subatom(p):
    '''subatom : subsubatom
               | subatom subatom'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'{p[2]}'
    elif len(p) == 3:
        p[0] = f'{p[1]} {p[2]}'


def p_atom(p):
    '''atom : id
            | id subatom'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = f'{p[1]} {p[2]}'


def p_block(p):
    '''block : atom
             | LBR or RBR'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]


def p_and(p):
    '''and : block
           | block AND and'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'AND ({p[1]}) ({p[3]})'


def p_or(p):
    '''or : and
          | and OR or'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'OR ({p[1]}) ({p[3]})'


def p_error(p):
    raise SyntaxError


def to_parse(string):
    parser = yacc.yacc()
    lexemes = string.split('.')
    for i in range(len(lexemes) - 1):
        lexemes[i] += '.'
    output = ''
    for lexeme in lexemes:
        if lexeme.strip() == '':
            continue
        try:
            ans = parser.parse(lexeme)
        except SyntaxError:
            return f'Something went wrong in:\n\n{lexeme.strip()}\n'
        output += ans + '\n'
    return output


def main(filename: str):
    with open(filename, 'r') as file:
        string = file.read()

    with open(filename[0 : -3] + 'out', 'w') as file:
        file.write(to_parse(string))


if __name__ == '__main__':
    main(sys.argv[1])

