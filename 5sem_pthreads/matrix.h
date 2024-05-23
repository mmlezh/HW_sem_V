#ifndef matrix_h
#define matrix_h

#include <sys/resource.h>
#include <sys/time.h>

#include<math.h>
#include<stdio.h>
#include<stdlib.h>

#define EROUT 1


int fmatin(int size, double *A, int *inds, FILE *input); //+
void fmatout(int amount, int size, double *A, FILE *output); //+

void generateMatrix(int size, int numout, double *A, int *inds); //+
double f(int i, int j, int nmout, int size); //+

long int get_time(void); //+
long int get_full_time(void); //+

#endif