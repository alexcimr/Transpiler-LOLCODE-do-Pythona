# Projekt: Transpiler LOLCODE do Pythona

### Dane studentów i kontakt
Alex Cimr - alexcimr@student.agh.edu.pl \
Piotr Ciećkiewicz - pcieckiewicz@student.agh.edu.pl

---

### Założenia projektu

**Krótki opis:**
Głównym założeniem projektu jest stworzenie narzędzia do automatycznej translacji kodu źródłowego z języka LOLCODE na język Python. Program ma za zadanie interpretować składnię specyfikacji LOLCODE i przekładać ją na konstrukcje logiczne w środowisku Python.

**Ogólne cele programu:**
Projekt koncentruje się na przeprowadzeniu pełnej analizy leksykalnej oraz składniowej plików źródłowych. Kluczowym celem jest poprawne odwzorowanie struktur danych, zmiennych oraz mechanizmów sterowania przepływem (takich jak pętle i instrukcje warunkowe) na czytelny kod wynikowy.

**Rodzaj translatora:**
*Transpiler*

**Planowany wynik działania:**
Wynikiem pracy narzędzia jest konwerter LOLCODE do Pythona. Aplikacja przyjmuje pliki z rozszerzeniem .lol, a następnie generuje funkcjonalny i gotowy do samodzielnego uruchomienia skrypt .py, który zachowuje pełną logikę pierwotnego programu.

**Język implementacji:**
*Python*

**Sposób realizacji skanera oraz parsera:**
Analiza leksykalna (skaner) i składniowa (parser) zostanie wykonana przy użyciu biblioteki PLY, wykorzystując odpowiednio jej moduły Lex oraz Yacc.
