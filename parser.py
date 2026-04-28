import ply.yacc as yacc
from lexer import tokens

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
