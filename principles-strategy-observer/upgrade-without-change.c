#include <stddef.h>
#include <stdio.h>
#include <string.h>

const void *mymax(
    const void *base, size_t nmemb, size_t size,
    int (*compar)(const void *, const void *)) {
        if (nmemb == 0) return NULL;

        const char *max = (const char*) base;
        const char *current = max;

        for (int i = 1; i < nmemb; i++) {
            current += size;
            if (compar(current, max) > 0) {
                max = current;
            }
        }

        return max;
    }

int gt_int(const void *first, const void *second) {
    int a = *(const int*) first;
    int b = *(const int*) second;
    if (a > b) return 1;
    if (a < b) return -1;
    return 0;
}

int gt_char(const void *first, const void *second) {
    const char a = *(const char*) first;
    const char b = *(const char*) second;
    if (a > b) return 1;
    if (a < b) return -1;
    return 0;
}

int gt_str(const void *first, const void *second) {
    const char *a = *(const char* const*) first;
    const char *b = *(const char* const*) second;
    return strcmp(a, b);
}

int main() {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[]="Suncana strana ulice";
    const char* arr_str[] = { "Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"};

    const int* int_max = (const int*) mymax(&arr_int, 9, sizeof(arr_int[0]), gt_int);
    printf("Int max: %d\n", *int_max);

    const char* char_max = (const char*) mymax(&arr_char, strlen(arr_char), sizeof(arr_char[0]), gt_char);
    printf("Char max: %c\n", *char_max);

    const char* str_max = *(const char* const*) mymax(arr_str, 11, sizeof(arr_str[0]), gt_str);
    printf("Str max: %s\n", str_max);
}