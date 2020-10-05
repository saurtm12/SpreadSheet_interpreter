#!/usr/bin/env python3

import sys, ply.lex
import re
tokens = ('ASSIGN',
        'LPAREN', 'RPAREN',
        'LSQUARE','RSQUARE',
        'LCURLY', 'RCURLY',
        'COMMA',
        'DOTDOT',
        'SQUOTE',
        'COLON',
        'DOLLAR',
        'NUMBER_SIGN',
        'EQ',
        'NOTEQ',
        'LT', 'LTEQ',
        'GT', 'GTEQ',
        'PLUS',
        'MINUS',
        'MULT',
        'DIV',
        'INFO_STRING',
        'COORDINATE_IDENT',
        'DECIMAL_LITERAL',
        'INT_LITERAL',
        'IDENT',
        'RANGE_IDENT',
        'SHEET_IDENT',
        'FUNC_IDENT',
        #keywords:
        'SHEET',
        'SCALAR',
        'RANGE',
        'DO',
        'DONE',
        'IS',
        'WHILE',
        'FOR',
        'IF',
        'THEN',
        'ELSE',
        'ENDIF',
        'FUNCTION',
        'SUBROUTINE',
        'RETURN',
        'END',
        'PRINT_SHEET',
        'PRINT SCALAR',
        'PRINT_RANGE'
        )

t_SHEET = 'sheet'
t_SCALAR = 'scalar'
t_RANGE = 'range'
t_DO = 'do'
t_DONE = 'done'
t_IS = 'is'
t_WHILE = 'while'
t_FOR = 'for'
t_IF = 'if'
t_THEN = 'then'
t_ELSE = 'else'
t_ENDIF = 'endif'
t_FUNCTION = 'function'
t_SUBROUTINE = 'subroutine'
t_RETURN = 'return'
t_END = 'end'
t_PRINT_SHEET = 'print_sheet'
t_PRINT_SCALAR = 'print_scalar'
t_PRINT_RANGE = 'print_range'

t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'{'
t_RCURLY = r'}'

t_COMMA = r','
t_DOTDOT = r'\.\.'
t_SQUOTE = r"'"
t_COLON = r':'
t_DOLLAR = r'\$'
t_NUMBER_SIGN = r'\#'

t_EQ = r'='
t_NOTEQ = r'!='
t_LT = r'<'
t_LTEQ = r'<='
t_GT = r'>'
t_GTEQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

def t_INFO_STRING(t):
    r'!.*?!'
    t.value = t.value[1:-1]
    return t

def t_COORDINATE_IDENT(t):
    r'([A-Z]{1,2}[0-9]{1,3})\s'
    t.value = t.value[:-1]
    return t

def t_DECIMAL_LITERAL(t):
    r'-?\d+\.\d'
    try:
        t.value = float(t.value)
    except ValueError:
        print('Float is too large')
        t.value =0
    return t

def t_INT_LITERAL(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_IDENT(t):
    r'[a-z][a-zA-Z0-9_]+'
    return t

def t_RANGE_IDENT(t):
    r'_[a-zA-Z0-9_]+'
    return t

def t_SHEET_IDENT(t):
    r'[A-Z]+'
    return t

def t_FUNC_IDENT(t):
    r'[A-Z][a-z0-9_]+'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_COMMENT(t):
    r"\.{3,3}([\s\S]*?)\.{3,3}"
    pass

def t_error(t):
    raise Exception("Illegal character '{}' at line {}".format( 
        t.value[0], t.lexer.lineno ) )

lexer = ply.lex.lex()

if __name__ == '__main__':
    import argparse, codecs
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who == True:
        print( '292119 Nghia Duc Hong' )
    elif ns.file is None:
        parser.print_help()
    else:
        with codecs.open( ns.file, 'r', encoding='utf-8' ) as INFILE:
            data = INFILE.read() 
        #pre eliminate comments 
        data = re.sub(r"\.{3,3}([\s\S]*?)\.{3,3}","",data)
        lexer.input( data )

        while True:
            token = lexer.token()
            if token is None:
                break
            print( token )
