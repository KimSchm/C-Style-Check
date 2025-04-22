#include <stdio.h>
#include <stdlib.h>

// Deklaration der Funktion zum Sortieren des Arrays
void bubbleSort(short int* array, int size);

int main() {
    // Allokation von Speicher fr 100 short ints
    short int* zahlen = malloc(sizeof(short int) * 100);

    // Zweiter Zeiger zum Schreiben in das Array
    short int** schreibzeiger = zahlen;

    // Befllen des Arrays mit Werten von 100 bis 1
    for (int i = 0; i < 100; i++) {
        *schreibzeiger++ = 100 - i;
    }

    // Ausgabe des unsortierten Arrays
    printf("Unsortiertes Array:\n");
    for (int i = 0; i < 100; i++) {
        printf("%d ", zahlen[i]);
    }
    printf("\n\n");

    // Sortieren des Arrays mit BubbleSort
    bubbleSort(zahlen, 100);

    // Ausgabe des sortierten Arrays
    printf("Sortiertes Array:\n");
    for (int i = 0; i < 100; i++) {
        printf("%d ", zahlen[i]);
    }
    printf("\n");

    // Freigabe des Speicherplatzes
    free(zahlen);

    return 0;
}

// Funktion zum Sortieren des Arrays mit BubbleSort
void bubbleSort(short int* array, int size) {
    int i, j;
    for (i = 0; i < size - 1; i++) {
        for (j = 0; j < size - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                // Tauschen der Elemente
                short int temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            }
        }
    }
}

// Kommentar zur Verbesserung der Laufzeit von BubbleSort:

// Wenn das Array bereits weitestgehend vorsortiert ist, kann die Laufzeit von BubbleSort 
// durch die Verwendung einer Abbruchbedingung deutlich verbessert werden. 
// Die Abbruchbedingung kann prfen, ob in einem Durchlauf keine Tauschungen 
// stattgefunden haben. In diesem Fall ist das Array bereits sortiert und der 
// Sortiervorgang kann abgebrochen werden.