#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Unary Function
typedef struct Unary_Function_VTable {
    double (*value_at) (void* self, double* x);
    double (*negative_value_at) (void* self, double* x);
} Unary_Function_VTable;

typedef struct {
    int lower_bound;
    int upper_bound;
    Unary_Function_VTable* UF_VTable;
} Unary_Function;

double uf_negative_value_at(void* self, double* x) {
    Unary_Function* uf = (Unary_Function*) self;
    return -uf->UF_VTable->value_at(uf, x);
}

void uf_tabulate(Unary_Function* uf) {
    for (int i = uf->lower_bound; i < uf->upper_bound; i++) {
        double dbl = (double) i;
        printf("f(%d) = %f \n", i, uf->UF_VTable->value_at(uf, &dbl));
    }
    printf("---------------- \n");
}

bool same_functions_for_ints(Unary_Function* f1, Unary_Function* f2, double tolerance) {
    if (f1->lower_bound != f2->lower_bound) return false;
    if (f1->upper_bound != f2->upper_bound) return false;

    for (int i = f1->lower_bound; i < f2->upper_bound; i++) {
        double dbl = (double) i;
        double delta = f1->UF_VTable->value_at(f1, &dbl) - f2->UF_VTable->value_at(f2, &dbl);
        if(delta < 0) delta = -delta;
        if(delta > tolerance) return false;
    }

    return true;
}

// Square Function
double square_value_at(void* self, double* x) {
    return *x * *x;
}

Unary_Function_VTable Square_VTable = {
    square_value_at,
    uf_negative_value_at
};

typedef struct {
    Unary_Function base;
} Square;

void construct_square(Square* sq, int lower_bound, int upper_bound) {
    sq->base.lower_bound = lower_bound;
    sq->base.upper_bound = upper_bound;
    sq->base.UF_VTable = &Square_VTable;
}

// Linear Function
typedef struct {
    Unary_Function base;
    double a;
    double b;
} Linear;

double linear_value_at(void* self, double* x) {
    Linear* linear = (Linear*) self;
    return linear->a * *x + linear->b;
}

Unary_Function_VTable Linear_VTable = {
    linear_value_at,
    uf_negative_value_at
};

void construct_linear(Linear* linear, int lower_bound, int upper_bound, double a, double b) {
    linear->a = a;
    linear->b = b;
    linear->base.lower_bound = lower_bound;
    linear->base.upper_bound = upper_bound;
    linear->base.UF_VTable = &Linear_VTable;
}

// malloc methods for Square and Linear
Square* createSquare(int lower, int upper) {
    Square* square = malloc(sizeof(Square));
    construct_square(square, lower, upper);
    return square;
}

Linear* createLinear(int lower, int upper, double a, double b) {
    Linear* linear = malloc(sizeof(Linear));
    construct_linear(linear, lower, upper, a, b);
    return linear;
}

void print_function_value_at(char name[], Unary_Function* func, double at) {
    printf("%s f() at %f = %f \n", name, at, func->UF_VTable->value_at(func, &at));
}

int main() {
    Square* heapSquare = createSquare(1, 10);
    Square stackSquare;
    construct_square(&stackSquare, 1, 10);

    uf_tabulate((Unary_Function*) heapSquare);

    Linear* heapLinear = createLinear(1, 10, 2, 3);
    Linear stackLinear;
    construct_linear(&stackLinear, 1, 10, 2, 3);

    uf_tabulate((Unary_Function*) heapLinear);

    double valAt = 5;
    
    print_function_value_at("Square", (Unary_Function*) heapSquare, valAt);
    print_function_value_at("Linear", (Unary_Function*) heapLinear, valAt);

    return 0;
}

