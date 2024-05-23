#include "matrix.h"

//==============================================//

int fmatin(int size, double *A, int *inds, FILE *input)//O(n^2)
{
	for(int i = 0; i < size; i++)
	{
		for(int j = 0; j < size; j++)
		{
			double temp;
			if((fscanf(input, "%lf", &temp)) != 1)
			{
				return EROUT;
			}
			A[i*size + j] = temp;
		}
		inds[i] = i;
	}

	return 0;
}


void fmatout(int amount, int size, double *A, FILE *output)//O(n^2)
{
	for(int i = 0; i < amount; i++)
	{
		fprintf(output, "\n\t");
		for(int j = 0; j < amount; j++)
		{
			// fprintf(output, "%10.3e\t", A[j+i*size]);	
			fprintf(output, "%.2lf\t", A[j+i*size]);
		}
	}
	fprintf(output,"\n");
}


void generateMatrix(int size, int numout, double *A, int *inds)//O(n^2)
{
	for(int i = 0; i < size; i++)
	{
		for(int j = 0; j < size; j++)
		{
			A[i*size + j] = f(i+1, j+1, numout, size);
		}
		inds[i] = i;
	}
}

double f(int i, int j, int numout, int size) // заранее проверяем k
{
	int max;
	max = i > j ? i : j;
	switch (numout)
	{
		case 1: 
			return size - max + 1;
		case 2:
			return max;
		case 3: 
			return abs(i-j);
		default: 
			return 1.0/(i+j-1);
	}
}


long int get_time(void) //+
{
	struct rusage buf;

	getrusage(RUSAGE_SELF, &buf);

	return buf.ru_utime.tv_sec * 100 + buf.ru_utime.tv_usec/10000;
}

long int get_full_time(void) //+
{
	struct timeval buf;

	gettimeofday(&buf, 0);

	return buf.tv_sec * 100 + buf.tv_usec/10000;
}