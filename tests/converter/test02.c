#include <stdio.h>
#include <stdlib.h>

/* Was
ist
 den
* hier los?
*/ 


// Definition der Struktur und Typen
typedef struct MonthlySalary {
    unsigned int uiEmployeeNumber;
    float fSalary;
} sMonthlySalary_t;

typedef sMonthlySalary_t* psMonthlySalary_t;

// Prototypen der Funktionen
int compareFloats(const float* a, const float* b);
int compareMonthlySalaries(const void* a, const void* b);
void printArray(float* arr, int size);
void printMonthlySalaryArray(sMonthlySalary_t* arr, int size);

int main() {
    // Initialisierung der Arrays
    long int bla = 0;
    float salaries[10] = { 8000.0f, 6500.0f, 9200.0f, 7800.0f, 5700.0f,
                         4900.0f, 10200.0f, 5400.0f, 7100.0f, 6200.0f };

    sMonthlySalary_t monthlySalaries[10] = {
        {1, salaries[0]}, {2, salaries[1]}, {3, salaries[2]}, {4, salaries[3]},
        {5, salaries[4]}, {6, salaries[5]}, {7, salaries[6]}, {8, salaries[7]},
        {9, salaries[8]}, {10, salaries[9]} };

    bla = 4;
    
    // Sortierung der Arrays
    qsort(salaries, 10, sizeof(float), compareFloats);
    qsort(monthlySalaries, 10, sizeof(sMonthlySalary_t), compareMonthlySalaries);

    // Ausgabe der sortierten Arrays
    printf("Sortierte Float-Array:\n");
    printArray(salaries, 10);

    printf("\nSortierte MonthlySalary-Array:\n");
    printMonthlySalaryArray(monthlySalaries, 10);

    return 0;
}

// Vergleichsfunktion fr Floats
int compareFloats(const float* a, const float* b) {
    if (*a < *b) {
        return -1;
    }
    else if (*a > *b) {
        return 1;
    }
    else {
        return 0;
    }
}

// Vergleichsfunktion fr MonthlySalary-Strukturen
int compareMonthlySalaries(const void* a, const void* b) {
    sMonthlySalary_t* s1 = (sMonthlySalary_t*)a;
    sMonthlySalary_t* s2 = (sMonthlySalary_t*)b;

    if (s1->fSalary < s2->fSalary) {
        return -1;
    }
    else if (s1->fSalary > s2->fSalary) {
        return 1;
    }
    else {
        return 0;
    }
}

// Funktion zum Ausdrucken eines Float-Arrays
void printArray(float* arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%.2f ", arr[i]);
    }
    printf("\n");
}

// Funktion zum Ausdrucken eines MonthlySalary-Arrays
void printMonthlySalaryArray(sMonthlySalary_t* arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("Mitarbeiter %d: %.2f Gehalt\n", arr[i].uiEmployeeNumber, arr[i].fSalary);
    }
}
