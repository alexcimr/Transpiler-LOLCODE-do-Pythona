import ply.lex as lex
import ply.yacc as yacc
import sys

#SKANER
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


#PARSER
def p_program(p):
    """program : HAI separator statements KTHXBYE
               | HAI separator KTHXBYE"""
    if len(p) == 5:
        kod_py = "\n".join([stmt for stmt in p[3] if stmt is not None])
        p[0] = f"# --- Wygenerowano z LOLCODE ---\n\n{kod_py}"
    else:
        p[0] = "# Pusty program"

def p_statements(p):
    """statements : statements statement
                  | statement"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    """statement : declaration separator
                 | print separator
                 | expression separator"""
    p[0] = p[1]

def p_separator(p):
    """separator : NEWLINE
                 | separator NEWLINE"""
    pass

def p_declaration(p):
    """declaration : VAR_DEC ID
                   | VAR_DEC ID ITZ expression"""
    if len(p) == 3:
        p[0] = f"{p[2]} = None"
    else:
        p[0] = f"{p[2]} = {p[4]}"

def p_print(p):
    """print : VISIBLE arg_list"""
    p[0] = f"print({p[2]})"

def p_arg_list(p):
    """arg_list : expression"""
    p[0] = p[1]

def p_expression(p):
    """expression : math_expr
                  | ID
                  | literal"""
    p[0] = str(p[1])

def p_literal(p):
    """literal : NUMBR
               | YARN"""
    p[0] = p[1]

def p_math_expr(p):
    """math_expr : SUM expression AN expression"""
    p[0] = f"({p[2]} + {p[4]})"

def p_error(p):
    if p:
        print(f"Błąd składniowy przy tokenie '{p.value}' (linia {p.lineno})")
    else:
        print("Błąd składniowy: Niespodziewany koniec pliku")

parser = yacc.yacc()


#URUCHOMIENIE
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Użycie: python transpiler.py wejscie.lol wyjscie.py")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        kod_lol = f.read()

    wynik = parser.parse(kod_lol, lexer=lexer)

    if wynik:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(wynik)
        print(f"Wygenerowano plik: {sys.argv[2]}")
