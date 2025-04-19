# C-Style-Check
C-Style-Check ist ein Tool, das den C-Code auf Stilkonventionen überprüft.

## Checks
- [x] A4: Kommentare beginnen mit einem //. Mehrzeilige Kommentare /* */ sind nicht erlaubt.
- [ ] A5: Dateinamen beginnen mit einem Großbuchstaben.
- [ ] A6: Eine Funktion darf maximal nur 4-40 Programmzeilen enthalten.
- [x] A7: Eine C-Datei darf maximal nur 4-400 Zeilen enthalten.
- [ ] A8: Eine C-Datei (Modul) ist wie folgt aufgebaut:
   1. Systemheaderdateien (z.B. #include <stdio.h>)
   2. User Headerdateien (z.B. #include "Eightqueen.h")
   3. Modulspezifische Datentypen: Defines, Konstanten, Enumerationen, Structs, Unions, Bitfields, Typedefs, Makros
   4. Externe und globale Variablen (Ausnahmefall)
   5. Funktionsdeklarationen für alle Funktionen außer main
   6. Funktionsimplementierungen (Die main-Funktion wird in einem Modul immer als erste Funktion implementiert.)
- [x] CL1: Die öffnende { und schließende } geschweifte Klammer beginnt stets in einer neuen Zeile.
- [x] CL5: Operatoren müssen durch Leerzeichen getrennt sein (z.B. `a + b` statt `a+b`).
- [ ] DV3 II: Bei Variablennamen ist die Ungarische Notation als Präfix zu verwenden. z.B.:
    - short int: si
    - unsigned short int: usi
    - int: i
    - unsigned int: ui
    - long int: li
    - unsigned long int: uli
    - long long int: lli
    - unsigned long long int: ulli
    - signed char: c
    - unsigned char: uc
    - float: f
    - double: d
    - long double: ld
    - _Bool (C99 native): b