# Projekt: Transpiler LOLCODE do Pythona

### Dane studentów i kontakt
* Alex Cimr - alexcimr@student.agh.edu.pl
* Piotr Ciećkiewicz - pcieckiewicz@student.agh.edu.pl

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



## Gramatyka Języka (Notacja Yacc)
Poniżej znajduje się formalna specyfikacja składni, która posłuży do wygenerowania parsera.

```ebnf
program : HAI opt_version separator statements KTHXBYE

opt_version : FLOAT
            | empty

statements : statements statement
           | statement

statement : declaration separator
          | assignment separator
          | print separator
          | input separator
          | expression separator
          | if_block separator
          | loop_block separator

separator : NEWLINE
          | COMMA
          | separator NEWLINE
          | separator COMMA

Zmienne i Przypisania:

declaration : I HAS A IDENTIFIER
            | I HAS A IDENTIFIER ITZ expression

assignment : IDENTIFIER R expression

Wejście / Wyjście:

print : VISIBLE print_args

print_args : expression
           | print_args expression

input : GIMMEH IDENTIFIER

Wyrażenia i Literały:

expression : math_expr
           | bool_expr
           | comp_expr
           | IDENTIFIER
           | literal

literal : INTEGER 
        | FLOAT  
        | STRING 
        | BOOLEAN

Operacje Matematyczne:

math_expr : SUM OF expression AN expression
          | DIFF OF expression AN expression
          | PRODUKT OF expression AN expression
          | QUOSHUNT OF expression AN expression
          | MOD OF expression AN expression
          | BIGGR OF expression AN expression
          | SMALLR OF expression AN expression

Operacje Logiczne:

bool_expr : BOTH OF expression AN expression
          | EITHER OF expression AN expression
          | WON OF expression AN expression
          | NOT expression

Operacje Porównania:

comp_expr : BOTH SAEM expression AN expression
          | DIFFRINT expression AN expression

Sterowanie Przepływem (IF/ELSE):

if_block : O_RLY separator YA_RLY separator statements OIC
         | O_RLY separator YA_RLY separator statements NO_WAI separator statements OIC

Pętle:

loop_block : IM_IN_YR IDENTIFIER loop_op loop_cond separator statements IM_OUTTA_YR IDENTIFIER

loop_op : UPPIN YR IDENTIFIER
        | NERFIN YR IDENTIFIER
        | empty

loop_cond : TIL expression
          | WILE expression
          | empty

Espilon:

empty :
