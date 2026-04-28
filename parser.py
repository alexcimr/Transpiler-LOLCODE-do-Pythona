import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    """program : HAI separator statements KTHXBYE optional_separator
               | HAI separator KTHXBYE optional_separator"""
    if len(p) == 6:
        clean_statements = [s for s in p[3] if s is not None]
        p[0] = "\n".join(clean_statements)
    else:
        p[0] = ""

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
                 | expression separator
                 | NEWLINE"""
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[1]

def p_declaration(p):
    """declaration : VAR_DEC ID
                   | VAR_DEC ID ITZ expression"""
    if len(p) == 3:
        p[0] = f"{p[2]} = None"
    else:
        p[0] = f"{p[2]} = {p[4]}"

def p_print(p):
    """print : VISIBLE expression"""
    p[0] = f"print({p[2]})"

def p_expression(p):
    """expression : math_expr
                  | ID
                  | literal"""
    p[0] = str(p[1])

def p_math_expr(p):
    """math_expr : SUM expression AN expression"""
    p[0] = f"({p[2]} + {p[4]})"

def p_literal(p):
    """literal : NUMBR
               | YARN"""
    if isinstance(p[1], str):
        p[0] = f'"{p[1]}"'
    else:
        p[0] = p[1]

def p_separator(p):
    """separator : NEWLINE"""
    pass

def p_optional_separator(p):
    """optional_separator : separator
                          | empty"""
    pass

def p_empty(p):
    """empty :"""
    pass

def p_error(p):
    if p:
        print(f"Błąd składniowy: token '{p.value}' w linii {p.lineno}")
    else:
        print("Błąd składniowy: Koniec pliku")

parser = yacc.yacc()