import ply.yacc as yacc
from lexer import tokens

def indent(block):
    if not block or not block.strip():
        return "    pass"
    return "\n".join("    " + line for line in block.split("\n") if line.strip())


def p_program(p):
    """program : HAI separator statements KTHXBYE optional_separator
               | HAI separator KTHXBYE optional_separator"""
    if len(p) == 6:
        p[0] = p[3]
    else:
        p[0] = "pass"


def p_statements(p):
    """statements : statements statement
                  | statement"""
    if len(p) == 3:
        prev = p[1] or ""
        if p[2] is not None:
            p[0] = (prev + "\n" + p[2]).strip("\n")
        else:
            p[0] = prev
    else:
        p[0] = p[1] if p[1] is not None else ""


def p_statement(p):
    """statement : declaration separator
                 | assignment separator
                 | print separator
                 | input separator
                 | expression separator
                 | if_block separator
                 | loop_block separator
                 | gtfo separator
                 | NEWLINE
                 | COMMENT separator"""
    if p.slice[1].type == 'COMMENT':
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = None
    elif p.slice[1].type == 'expression':
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
        p[0] = f"{p[2]} = {{}}"
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
    if len(p[2]) == 1:
        p[0] = f"print({p[2][0]})"
    else:
        concat = " + ".join(f"str({a})" for a in p[2])
        p[0] = f"print({concat})"


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
    if len(p) == 3:
        concat = " + ".join(f"str({a})" for a in p[2])
        p[0] = f"({concat})"
    else:
        p[0] = str(p[1])


def p_literal(p):
    """literal : NUMBR
               | NUMBAR
               | YARN
               | WIN
               | FAIL
               | NOOB"""
    token_type = p.slice[1].type
    if token_type == 'YARN':
        escaped = p[1].replace("\\", "\\\\").replace('"', '\\"')
        p[0] = f'"{escaped}"'
    elif token_type == 'WIN':
        p[0] = "True"
    elif token_type == 'FAIL':
        p[0] = "False"
    elif token_type == 'NOOB':
        p[0] = "None"
    else:
        p[0] = str(p[1])


_MATH_OPS = {
    'SUM': '+', 'DIFF': '-', 'PRODUKT': '*', 'QUOSHUNT': '/', 'MOD': '%'
}

def p_math_expr(p):
    """math_expr : SUM expression AN expression
                 | DIFF expression AN expression
                 | PRODUKT expression AN expression
                 | QUOSHUNT expression AN expression
                 | MOD expression AN expression
                 | BIGGR expression AN expression
                 | SMALLR expression AN expression"""
    keyword = p[1].split()[0]
    if keyword == 'BIGGR':
        p[0] = f"max({p[2]}, {p[4]})"
    elif keyword == 'SMALLR':
        p[0] = f"min({p[2]}, {p[4]})"
    else:
        p[0] = f"({p[2]} {_MATH_OPS[keyword]} {p[4]})"


def p_bool_expr(p):
    """bool_expr : BOTH_OF expression AN expression
                 | EITHER_OF expression AN expression
                 | WON_OF expression AN expression
                 | NOT expression
                 | ALL_OF arg_list MKAY
                 | ANY_OF arg_list MKAY"""
    keyword = p[1].split()[0]
    if keyword == 'BOTH':
        p[0] = f"({p[2]} and {p[4]})"
    elif keyword == 'EITHER':
        p[0] = f"({p[2]} or {p[4]})"
    elif keyword == 'WON':
        p[0] = f"(bool({p[2]}) != bool({p[4]}))"
    elif keyword == 'NOT':
        p[0] = f"(not {p[2]})"
    elif keyword == 'ALL':
        p[0] = f"all([{', '.join(p[2])}])"
    elif keyword == 'ANY':
        p[0] = f"any([{', '.join(p[2])}])"


def p_comp_expr(p):
    """comp_expr : BOTH_SAEM expression AN expression
                 | DIFFRINT expression AN expression"""
    if p[1].split()[0] == 'BOTH':
        p[0] = f"({p[2]} == {p[4]})"
    else:
        p[0] = f"({p[2]} != {p[4]})"


def p_if_block(p):
    """if_block : IF separator THEN separator statements mebbe_blocks else_block OIC"""
    code = "if _IT:\n" + indent(p[5])
    if p[6]:
        code += "\n" + p[6]
    if p[7] is not None:
        code += "\nelse:\n" + indent(p[7])
    p[0] = code


def p_mebbe_blocks(p):
    """mebbe_blocks : mebbe_blocks MEBBE expression separator statements
                    | empty"""
    if len(p) == 6:
        new_elif = f"elif {p[3]}:\n{indent(p[5])}"
        p[0] = (p[1] + "\n" + new_elif) if p[1] else new_elif
    else:
        p[0] = ""


def p_else_block(p):
    """else_block : ELSE separator statements
                  | empty"""
    p[0] = p[3] if len(p) == 4 else None


def p_loop_block(p):
    """loop_block : LOOP_START ID loop_op loop_cond separator statements LOOP_END ID"""
    cond_code = p[4] if p[4] else "True"
    code = f"while {cond_code}:\n" + indent(p[6])
    if p[3]:
        _, op_code = p[3]
        code += "\n" + indent(op_code)
    p[0] = code


def p_loop_op(p):
    """loop_op : UPPIN YR ID
               | NERFIN YR ID
               | empty"""
    if len(p) == 4:
        p[0] = (p[3], f"{p[3]} += 1") if p[1] == 'UPPIN' else (p[3], f"{p[3]} -= 1")
    else:
        p[0] = None


def p_loop_cond(p):
    """loop_cond : TIL expression
                 | WILE expression
                 | empty"""
    if len(p) == 3:
        p[0] = f"not ({p[2]})" if p[1] == 'TIL' else f"({p[2]})"
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
    p[0] = None


def p_error(p):
    if p:
        raise SyntaxError(
            f"Błąd składniowy w linii {p.lineno}"
        )
    else:
        raise SyntaxError("Błąd składniowy: koniec pliku")


parser = yacc.yacc()