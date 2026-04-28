import ply.lex as lex

tokens = (
    'HAI', 'KTHXBYE', 'NEWLINE', 
    'VAR_DEC', 'ITZ', 'VISIBLE', 
    'NUMBR', 'YARN', 'ID',
    'SUM', 'AN'
)

t_HAI = r'HAI'
t_KTHXBYE = r'KTHXBYE'
t_ITZ = r'ITZ'
t_VISIBLE = r'VISIBLE'
t_AN = r'AN'

def t_VAR_DEC(t):
    r'I\s+HAS\s+A'
    return t

def t_SUM(t):
    r'SUM\s+OF'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if t.value in ['HAI', 'KTHXBYE', 'ITZ', 'VISIBLE', 'AN']:
        t.type = t.value
    return t

def t_NUMBR(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_YARN(t):
    r'"[^"]*"'
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_COMMENT(t):
    r'BTW.*'
    pass

t_ignore = ' \t'

def t_error(t):
    print(f"Nieznany znak: '{t.value[0]}' w linii {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
