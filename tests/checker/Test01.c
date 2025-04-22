#include <stdio.h>
#include <stdlib.h>

#define DOSHOWOUTPUT 1

#define SMALLER10(Value1,Value2) (int)((((int)(Value1) + 10) < (int)(Value2)) ? (1) : (0))

// Makrodefinition
#define ABSOLUTE(x) (((x) < 0) ? (-x) : (x))

// Funktionsprototyp Funktion "print_absolute_value"
void print_absolute_value(int number);

int main(void) 
{
    int iX = 0;
    int iY = 10;

    printf("Hello World!\n");

#if DOSHOWOUTPUT
    printf("Hello user!\n");
#endif

    // Aufruf der Funktion "print_absolute_value"
    print_absolute_value(iX);
    print_absolute_value(iY);

    if (SMALLER10(iX, iY)) 
    {
        printf("First Value + 10 is smaller than second Value!\n");
    }

    // Warten auf Benutzereingabe
    _getch();

    return EXIT_SUCCESS;
}

// Funktion zum Drucken des absoluten Werts einer Zahl
void print_absolute_value(int number) 
{
    printf("Absolute Value of %d is: %d\n", number, ABSOLUTE(number));
}
