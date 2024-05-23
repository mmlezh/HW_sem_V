#ifndef matrix_h
#define matrix_h

#include<math.h>
#include<stdio.h>
#include<stdlib.h>

#define EROUT 1
#define EPS 2e-14

int fmatin(int size, double *A, int *inds, FILE *input);
void fmatout(int amount, int size, double *A, FILE *output);

void generateMatrix(int size, int numout, double *A, int *inds);
double f(int i, int j, int nmout, int size);

//==============================================//
void cswitch(int ind, int jnd, int size, double *A);
//==============================================//

int gsolve(int size, double *A, int *indr, double *res);
double residual(int size, double *A, double *res);

#endif
