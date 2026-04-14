# Projekt: Transpiler LOLCODE do Pythona

## Dane studentów i kontakt
* Alex Cimr - alexcimr@student.agh.edu.pl
* Piotr Ciećkiewicz - pcieckiewicz@student.agh.edu.pl

---

## Założenia projektu

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

## Opis tokenów

Skaner został zaimplementowany przy użyciu modułu `ply.lex`. Zgodnie z konwencją biblioteki, nazwy tokenów poprzedzone są przedrostkiem `t_`. Poniżej przedstawiono kompletną listę tokenów, ich wyrażenia regularne oraz ich znaczenie w specyfikacji LOLCODE.

#### Struktura programu i separatory
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_HAI` | `HAI` | Początek programu |
| `t_KTHXBYE` | `KTHXBYE` | Koniec programu |
| `t_NEWLINE` | `\n+` | Separator instrukcji |

#### Zmienne i przypisania
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_VAR_DEC` | `I HAS A` | Deklaracja nowej zmiennej |
| `t_ITZ` | `ITZ` | Inicjalizacja zmiennej (używane z `I HAS A`) |
| `t_R` | `R` | Operator przypisania nowej wartości |

#### Wejście / Wyjście
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_VISIBLE` | `VISIBLE` | Instrukcja wyjścia (print) |
| `t_GIMMEH` | `GIMMEH` | Instrukcja wejścia (input) |

#### Typy danych i literały
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_NUMBR` | `[0-9]+` | Liczba całkowita (Integer) |
| `t_NUMBAR` | `[0-9]+\.[0-9]+` | Liczba zmiennoprzecinkowa (Float) |
| `t_YARN` | `"[^"]*"` | Ciąg znaków (String) |
| `t_TROOSH_WIN`| `WIN` | Wartość logiczna Prawda (True) |
| `t_TROOSH_FAIL`| `FAIL` | Wartość logiczna Fałsz (False) |
| `t_NOOB` | `NOOB` | Wartość pusta (None/Null) |
| `t_ID` | `[a-zA-Z][a-zA-Z0-9_]*` | Identyfikator zmiennej lub etykiety |

#### Operatory arytmetyczne
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_SUM` | `SUM OF` | Dodawanie (+) |
| `t_DIFF` | `DIFF OF` | Odejmowanie (-) |
| `t_PRODUKT` | `PRODUKT OF` | Mnożenie (*) |
| `t_QUOSHUNT` | `QUOSHUNT OF` | Dzielenie (/) |
| `t_MOD` | `MOD OF` | Reszta z dzielenia (Modulo) |
| `t_BIGGR` | `BIGGR OF` | Zwraca większą z dwóch liczb (Max) |
| `t_SMALLR` | `SMALLR OF` | Zwraca mniejszą z dwóch liczb (Min) |
| `t_AN` | `AN` | Separator argumentów (używany m.in. w matematyce) |

#### Operatory logiczne i porównania
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_BOTH_SAEM` | `BOTH SAEM` | Operator równości (==) |
| `t_DIFFRINT` | `DIFFRINT` | Operator nierówności (!=) |
| `t_BOTH_OF` | `BOTH OF` | Logiczne AND |
| `t_EITHER_OF` | `EITHER OF` | Logiczne OR |
| `t_WON_OF` | `WON OF` | Logiczne XOR |
| `t_NOT` | `NOT` | Logiczna negacja (NOT) |
| `t_ALL_OF` | `ALL OF` | Logiczne AND dla nieskończ. liczby arg. |
| `t_ANY_OF` | `ANY OF` | Logiczne OR dla nieskończ. liczby arg. |
| `t_MKAY` | `MKAY` | Zamknięcie wyrażenia o zmiennej liczbie arg. |

#### Instrukcje warunkowe (If / Else)
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_IF` | `O RLY\?` | Otwarcie bloku instrukcji warunkowej |
| `t_THEN` | `YA RLY` | Blok wykonywany gdy warunek jest prawdziwy |
| `t_ELSE_IF` | `MEBBE` | Blok "Else If" |
| `t_ELSE` | `NO WAI` | Blok wykonywany gdy warunek jest fałszywy |
| `t_END_BLOCK` | `OIC` | Zamknięcie bloku warunkowego |

#### Pętle
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_LOOP_START`| `IM IN YR` | Otwarcie pętli z etykietą |
| `t_UPPIN` | `UPPIN` | Inkrementacja w pętli |
| `t_NERFIN` | `NERFIN` | Dekrementacja w pętli |
| `t_YR` | `YR` | Słowo łączące przy deklaracji zmiennej w pętli |
| `t_TIL` | `TIL` | Warunek końcowy "dopóki nie" (Until) |
| `t_WILE` | `WILE` | Warunek trwania "dopóki" (While) |
| `t_LOOP_END` | `IM OUTTA YR` | Zamknięcie pętli z etykietą |

#### Operacje na tekstach i komentarze
| Nazwa Tokena | Wyrażenie | Opis |
| :--- | :--- | :--- |
| `t_SMOOSH` | `SMOOSH` | Konkatenacja ciągów znaków |
| `t_COMMENT` | `BTW .*` | Komentarz jednolinijkowy (ignorowany) |
| `t_MULTI_START`| `OBTW` | Rozpoczęcie komentarza wielolinijkowego |
| `t_MULTI_END` | `TLDR` | Zakończenie komentarza wielolinijkowego |

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
