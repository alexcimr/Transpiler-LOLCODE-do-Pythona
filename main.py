from lexer import lexer
from parser import parser

def main():
    input_file = "test.lol"
    output_file = "out.py"

    with open(input_file, 'r', encoding='utf-8') as f:
        lol_code = f.read()

    lexer.lineno = 1
    python_result = parser.parse(lol_code, lexer=lexer)

    if python_result:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_result)
        print(f"Przetłumaczono z {input_file} do {output_file}")
    else:
        print("Translacja przerwana. W kodzie jest błąd.")

if __name__ == '__main__':
    main()