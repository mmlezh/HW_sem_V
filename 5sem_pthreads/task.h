#ifndef task_h
#define task_h

#include <pthread.h>
#include <math.h>

#define EPS 2e-14

//==============================================//

int invert(int size, double *A, double *res, int *indr, int my_rank, int total_threads);
double residual(int size, double *A, double *res);

#endif