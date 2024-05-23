#ifndef func_h
#define func_h

#include<math.h>
#include<stdio.h>
#include<stdlib.h>

#define EROUT 1
#define MachineEPS 1e-100 // 1e-100
#define MAXIT 1000000

int fmatin(int size, double *A,  FILE *input); // работает
void fmatout(int amount, int size, double *A, FILE *output); // работает
void fvectout(int size, double *v, FILE *output); // работает

void generateMatrix(int size, int numout, double *A); // работает
double f(int i, int j, int nmout, int size); // работает

//==============================================//

void Rot(int size, double *A);

double norma(int size, double *A);

int n_(int size, double* A, double l);

void EigenVal(int size, double *A, double *val, double EPS, int *iterOut);



#endif
