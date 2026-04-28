import sys
from lexer import lexer
from parser import parser

def main():
    if len(sys.argv) < 3:
        print("Użycie: python main.py <plik_wejsciowy.lol> <plik_wyjsciowy.py>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        lol_code = f.read()

    lexer.lineno = 1
    python_result = parser.parse(lol_code, lexer=lexer)

    if python_result:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_result)
        print(f"Wynik zapisano w: {output_file}")
    else:
        print("Translacja przerwana z powodu błędów składniowych.")

if __name__ == '__main__':
    main()
