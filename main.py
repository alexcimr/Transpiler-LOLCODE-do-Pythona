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
