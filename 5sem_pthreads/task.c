#include "task.h"
#include "synchronize.h"

//==============================================//

int invert(int size, double *A, double *res, int *indr, int my_rank, int total_threads) // переделать 
{
	int i; 
	int j; 
	int k;
    int indrMax;

	int temp;
	int first_row;
	int last_row;

	double tmp;


	for(i = 0; i < size; i++)
	{
		if(my_rank == 0)
		{
			indrMax = i;
			for(int j = i + 1; j < size; j++)
			{
				if(fabs(A[i * size + indrMax]) < fabs(A[i * size + j]))
				{
					indrMax = j;
				}
			}
			// нашли максимум
			j = indr[i];
			indr[i] = indr[indrMax];
			indr[indrMax] = j; 

			for(j = 0; j < size; j++)
			{
				
				tmp = A[j * size + i];
				A[j * size + i] = A[j * size + indrMax];
				A[j * size + indrMax] = tmp;
			}

			tmp = A[i * size + i];
			if(fabs(A[i*size + i]) < EPS) // матрица вырожденная 
			{
				tmp = -1;
			}

			tmp = 1.0/tmp;
			for(j = i; j < size; j++)
			{
				A[i * size + j] *= tmp;
			}
			for(j = 0; j < size; j++)
			{
				res[i * size + j] *= tmp;
			}
		}
		synchronize(total_threads);

		temp = (size - i - 1) * my_rank;
		first_row = temp/total_threads + i + 1;
		temp = (size - i - 1) * (my_rank + 1);
		last_row = temp/total_threads + i + 1;
        
//         temp= size * my_rank;
//         first_row = temp/total_threads;
//         temp = size * (my_rank + 1);
//         last_row = temp/total_threads;

		for (j = first_row; j < last_row; j++)
		{
			tmp = A[j * size + i];
			for (k = i; k < size; k++)
			{
				A[j * size + k] -= tmp * A[i * size + k];
			}
			for (k = 0; k < size; k++)
			{
				res[j * size + k] -= tmp * res[i * size + k];
			}
		}
		synchronize(total_threads);
	}	

	temp= size * my_rank;
	first_row = temp/total_threads;
	temp = size * (my_rank + 1);
	last_row = temp/total_threads;

	for(k = first_row; k < last_row; k++)
	{
		for(i = size - 1; i >= 0; i--)
		{
			tmp = res[i * size + k];
			for(j = i + 1; j < size; j++)
			{
				tmp -= A[i * size + j] * res[j * size + k];
			}
			res[i * size + k] = tmp;
		}
	}
	synchronize(total_threads);

	if(my_rank == 0)
	{
		for(i = 0; i < size; i++)
		{
			for(j = 0; j < size; j++)
			{
				A[indr[i] * size + j] = res[i * size + j];
			}
		}

		for(i = 0; i < size; i++)
		{
			for(j = 0; j < size; j++)
			{
				res[i * size + j] = A[i * size + j];
			}
		}
	}

	return 0;
}

double residual(int size, double *A, double *res) //распараллель
{
	double temp;
 	double result = 0.0;

 	for(int i = 0; i < size; i++)
 	{
 		for(int j = 0; j < size; j++)
 		{
 			temp = 0.0;
 			for(int k = 0; k < size; k++)
 			{
 				temp += A[i*size + k]*res[k*size + j];
 			}
 			if(i == j)
 			{
 				temp -= 1.0;
 			}
 			result += temp * temp;
 		}
 	}

 	return sqrt(result);
}

