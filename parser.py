import ply.yacc as yacc
from lexer import tokens


def indent(code_block):
    if not code_block:
        return ""
    return "\n".join("    " + line for line in code_block.split("\n") if line.strip())


def p_program(p):
    """program : HAI separator statements KTHXBYE optional_separator
               | HAI separator KTHXBYE optional_separator"""
    if len(p) >= 5 and p[3] != 'KTHXBYE':
        p[0] = p[3]
    else:
        p[0] = ""


def p_statements(p):
    """statements : statements statement
                  | statement"""
    if len(p) == 3:
        if p[2] is not None:
            p[0] = p[1] + "\n" + p[2]
        else:
            p[0] = p[1]
    else:
        p[0] = p[1] if p[1] else ""


def p_statement(p):
    """statement : declaration separator
                 | assignment separator
                 | print separator
                 | input separator
                 | expression separator
                 | if_block separator
                 | loop_block separator
                 | gtfo separator
                 | NEWLINE"""
    if len(p) == 2:
        p[0] = None
    else:
        if p.slice[1].type == 'expression':
            p[0] = f"_IT = {p[1]}"
        else:
            p[0] = p[1]


def p_declaration(p):
    """declaration : VAR_DEC ID
                   | VAR_DEC ID ITZ expression
                   | VAR_DEC ID ITZ BUKKIT"""
    if len(p) == 3:
        p[0] = f"{p[2]} = None"
    elif p[4] == 'BUKKIT':
        p[0] = f"{p[2]} = []"
    else:
        p[0] = f"{p[2]} = {p[4]}"


def p_assignment(p):
    """assignment : ID R expression
                  | ID AT expression R expression"""
    if len(p) == 4:
        p[0] = f"{p[1]} = {p[3]}"
    else:
        p[0] = f"{p[1]}[{p[3]}] = {p[5]}"


def p_print(p):
    """print : VISIBLE arg_list"""
    args = ", ".join(p[2])
    p[0] = f"print({args})"


def p_arg_list(p):
    """arg_list : expression
                | arg_list expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_input(p):
    """input : GIMMEH ID"""
    p[0] = f"{p[2]} = input()"


def p_expression(p):
    """expression : math_expr
                  | bool_expr
                  | comp_expr
                  | ID
                  | literal
                  | SMOOSH arg_list"""
    if len(p) == 2:
        p[0] = str(p[1])
    else:
        args = " + ".join([f"str({arg})" for arg in p[2]])
        p[0] = args


def p_literal(p):
    """literal : NUMBR
               | NUMBAR
               | YARN
               | WIN
               | FAIL
               | NOOB"""
    if isinstance(p[1], str) and p[1] not in ['True', 'False', 'None']:
        if p.slice[1].type == 'YARN':
            p[0] = f'"{p[1]}"'
        elif p[1] == 'WIN':
            p[0] = "True"
        elif p[1] == 'FAIL':
            p[0] = "False"
        elif p[1] == 'NOOB':
            p[0] = "None"
        else:
            p[0] = p[1]
    else:
        p[0] = p[1]


def p_math_expr(p):
    """math_expr : SUM expression AN expression
                 | DIFF expression AN expression
                 | PRODUKT expression AN expression
                 | QUOSHUNT expression AN expression
                 | MOD expression AN expression
                 | BIGGR expression AN expression
                 | SMALLR expression AN expression"""
    op = p[1].split()[0]
    if op == 'SUM':
        p[0] = f"({p[2]} + {p[4]})"
    elif op == 'DIFF':
        p[0] = f"({p[2]} - {p[4]})"
    elif op == 'PRODUKT':
        p[0] = f"({p[2]} * {p[4]})"
    elif op == 'QUOSHUNT':
        p[0] = f"({p[2]} / {p[4]})"
    elif op == 'MOD':
        p[0] = f"({p[2]} % {p[4]})"
    elif op == 'BIGGR':
        p[0] = f"max({p[2]}, {p[4]})"
    elif op == 'SMALLR':
        p[0] = f"min({p[2]}, {p[4]})"


def p_bool_expr(p):
    """bool_expr : BOTH_OF expression AN expression
                 | EITHER_OF expression AN expression
                 | WON_OF expression AN expression
                 | NOT expression
                 | ALL_OF arg_list MKAY
                 | ANY_OF arg_list MKAY"""
    op = p[1].split()[0]
    if op == 'BOTH':
        p[0] = f"({p[2]} and {p[4]})"
    elif op == 'EITHER':
        p[0] = f"({p[2]} or {p[4]})"
    elif op == 'WON':
        p[0] = f"(bool({p[2]}) != bool({p[4]}))"
    elif op == 'NOT':
        p[0] = f"(not {p[2]})"
    elif op == 'ALL':
        args = ", ".join(p[2])
        p[0] = f"all([{args}])"
    elif op == 'ANY':
        args = ", ".join(p[2])
        p[0] = f"any([{args}])"


def p_comp_expr(p):
    """comp_expr : BOTH_SAEM expression AN expression
                 | DIFFRINT expression AN expression"""
    op = p[1].split()[0]
    if op == 'BOTH':
        p[0] = f"({p[2]} == {p[4]})"
    elif op == 'DIFFRINT':
        p[0] = f"({p[2]} != {p[4]})"


def p_if_block(p):
    """if_block : IF separator THEN separator statements mebbe_blocks else_block OIC"""
    code = "if _IT:\n"
    code += indent(p[5])
    if p[6]:
        code += "\n" + p[6]
    if p[7]:
        code += "\nelse:\n"
        code += indent(p[7])
    p[0] = code


def p_mebbe_blocks(p):
    """mebbe_blocks : mebbe_blocks MEBBE expression separator statements
                    | empty"""
    if len(p) == 6:
        new_block = f"elif {p[3]}:\n{indent(p[5])}"
        p[0] = f"{p[1]}\n{new_block}" if p[1] else new_block
    else:
        p[0] = ""


def p_else_block(p):
    """else_block : ELSE separator statements
                  | empty"""
    if len(p) == 4:
        p[0] = p[3]
    else:
        p[0] = None


def p_loop_block(p):
    """loop_block : LOOP_START ID loop_op loop_cond separator statements LOOP_END ID"""
    loop_var, op_code = p[3] if p[3] else (None, None)
    cond_code = p[4] if p[4] else "True"
    body = p[6]

    code = f"while {cond_code}:\n"
    code += indent(body) + "\n"
    if op_code:
        code += indent(op_code)
    p[0] = code


def p_loop_op(p):
    """loop_op : UPPIN YR ID
               | NERFIN YR ID
               | empty"""
    if len(p) == 4:
        if p[1] == 'UPPIN':
            p[0] = (p[3], f"{p[3]} += 1")
        else:
            p[0] = (p[3], f"{p[3]} -= 1")
    else:
        p[0] = None


def p_loop_cond(p):
    """loop_cond : TIL expression
                 | WILE expression
                 | empty"""
    if len(p) == 3:
        if p[1] == 'TIL':
            p[0] = f"not ({p[2]})"
        else:
            p[0] = f"({p[2]})"
    else:
        p[0] = None


def p_gtfo(p):
    """gtfo : GTFO"""
    p[0] = "break"


def p_separator(p):
    """separator : NEWLINE
                 | separator NEWLINE"""
    p[0] = ""


def p_optional_separator(p):
    """optional_separator : separator
                          | empty"""
    pass


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if p:
        raise SyntaxError(
            f"Błąd składniowy w linii {p.lineno}"
        )
    else:
        raise SyntaxError("Błąd składniowy: koniec pliku")


parser = yacc.yacc()