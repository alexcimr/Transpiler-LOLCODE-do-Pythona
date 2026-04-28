import ply.lex as lex

tokens = (
    'HAI', 'KTHXBYE', 'NEWLINE',
    'VAR_DEC', 'ITZ', 'R', 'BUKKIT', 'AT',
    'VISIBLE', 'GIMMEH',
    'NUMBR', 'NUMBAR', 'YARN', 'WIN', 'FAIL', 'NOOB', 'ID',
    'SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD', 'BIGGR', 'SMALLR', 'AN',
    'BOTH_SAEM', 'DIFFRINT',
    'BOTH_OF', 'EITHER_OF', 'WON_OF', 'NOT',
    'ALL_OF', 'ANY_OF', 'MKAY',
    'IF', 'THEN', 'MEBBE', 'ELSE', 'OIC',
    'LOOP_START', 'UPPIN', 'NERFIN', 'YR', 'TIL', 'WILE', 'LOOP_END',
    'SMOOSH', 'GTFO'
)

# słowa kluczowe jednowyrazowe
keywords = {
    'HAI', 'KTHXBYE',
    'ITZ', 'R', 'BUKKIT', 'AT', 'VISIBLE', 'GIMMEH',
    'WIN', 'FAIL', 'NOOB', 'AN', 'NOT', 'MKAY',
    'MEBBE', 'OIC', 'DIFFRINT',
    'UPPIN', 'NERFIN', 'YR', 'TIL', 'WILE', 'SMOOSH',
    'GTFO'
}

# tokeny wielowyrazowe

def t_VAR_DEC(t):
    r'I\s+HAS\s+A'
    return t

def t_LOOP_START(t):
    r'IM\s+IN\s+YR'
    return t

def t_LOOP_END(t):
    r'IM\s+OUTTA\s+YR'
    return t

def t_BOTH_SAEM(t):
    r'BOTH\s+SAEM'
    return t

def t_BOTH_OF(t):
    r'BOTH\s+OF'
    return t

def t_EITHER_OF(t):
    r'EITHER\s+OF'
    return t

def t_WON_OF(t):
    r'WON\s+OF'
    return t

def t_ALL_OF(t):
    r'ALL\s+OF'
    return t

def t_ANY_OF(t):
    r'ANY\s+OF'
    return t

def t_SUM(t):
    r'SUM\s+OF'
    return t

def t_DIFF(t):
    r'DIFF\s+OF'
    return t

def t_PRODUKT(t):
    r'PRODUKT\s+OF'
    return t

def t_QUOSHUNT(t):
    r'QUOSHUNT\s+OF'
    return t

def t_MOD(t):
    r'MOD\s+OF'
    return t

def t_BIGGR(t):
    r'BIGGR\s+OF'
    return t

def t_SMALLR(t):
    r'SMALLR\s+OF'
    return t

def t_IF(t):
    r'O\s+RLY\?'
    return t

def t_THEN(t):
    r'YA\s+RLY'
    return t

def t_ELSE(t):
    r'NO\s+WAI'
    return t

def t_NUMBAR(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_NUMBR(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_YARN(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = t.value if t.value in keywords else 'ID'
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_COMMENT(t):
    r'BTW[^\n]*'
    pass

def t_MULTILINE_COMMENT(t):
    r'OBTW[\s\S]*?TLDR'
    t.lexer.lineno += t.value.count('\n')
    pass

t_ignore = ' \t'

def t_error(t):
    print(f"Błąd leksykalny: nieznany znak '{t.value[0]}' w linii {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()