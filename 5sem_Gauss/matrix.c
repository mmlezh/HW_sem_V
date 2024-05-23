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
			fprintf(output, "%10.3e\t", A[j+i*size]);	
			//fprintf(output, "%.2lf\t", A[j+i*size]);
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

//==============================================//

void cswitch(int ind, int jnd, int size, double *A) //O(n)
{
	for(int i = 0; i < size; i++)
	{
		double temp;
		temp = A[ind + i*size];
		A[ind + i*size] = A[jnd + i*size];
		A[jnd + i*size] = temp;
	}
}

//==============================================//

int gsolve(int size, double *A, int *indr, double *res)
{
	int indrMAX;
	int indTmp;
	double temp;
	double max;
	//double *recap;

	for(int i = 0; i < size; i++) //O(N^2)
	{
		for(int j = 0; j < size; j++)
		{
			res[i*size + j] = 0;
			if(i == j)
			{
				res[i*size + j] = 1;
			}
		}
	}

	for(int i = 0; i < size; i++)
	{
		max = fabs(A[i*size + i]);
		indrMAX = i;
		
		for(int j = i + 1; j < size; j++)
		{
			if(max < fabs(A[i*size + j]))
			{
				max = fabs(A[i*size + j]);
				indrMAX = j;
			}
		}
		//нашли наибольший по моделю элемент строки i
		

		//переставляем столбыцы(переменные)
		cswitch(i, indrMAX, size, A);

		indTmp = indr[i];
		indr[i] = indr[indrMAX];
		indr[indrMAX] = indTmp;

		// printf("\nНомер цикла %ld Перестановка : \n", i);
		// printf("\n A:");
		// fmatout(*A, stdout);
		// printf("res:\n");
		// fmatout(*res, stdout);

		if(fabs(A[i*size + i]) < EPS) // матрица вырожденная 
		{
			return 1;
		}

		// Шаг метода гауса
		//все делим на главный элемент строки
		temp = 1.0 / A[i*size + i];
		for (int j = i; j < size; j++)
		{
			A[i * size + j] *= temp;
		}

		for (int j = 0; j < size; j++)
		{
			res[i * size + j] *= temp;
		}

		//вычитаем строки
		for (int j = i + 1; j < size; j++)
		{
			temp = A[j * size + i];
			for (int k = i; k < size; k++)
			{
				A[j * size + k] -= A[i * size + k] * temp;

			}

			for (int k = 0; k < size; k++)
			{
				res[j * size + k] -= res[i * size + k] * temp;
			}
		}
	}
	

	//обратный ход метода гаусса
	for(int i = 0; i < size; i++) //обход по строке (выбор столбца)
	{
		for(int j = size; j>0; j--) //обход вверх по выбранному столбу
		{
			temp = res[(j-1)*size + i]; //запоминаем значение в i-ом столбце на j-ом месте
			for(int k = j; k < size; k++) //вычитаем все что ниже помноженные на соответствущие элементы столбца
			{
				temp -= A[(j-1)*size + k] * res[k*size + i];
				res[(j-1)*size + i] = temp;
			}
		}
	}



	for(int i = 0; i < size; i++)
	{	
		for(int j = 0; j < size; j++)
		{
			A[indr[i] * size + j] = res[i*size + j];
		}
	}

	for(int i = 0; i < size; i++)
	{	
		for(int j = 0; j < size; j++)
		{
			res[i*size + j] = A[i*size +j];
		}
	}

	return 0;
}

// double residual(int size, double *A, double *res)
// {
// 	double temp;
//  	double result = 0.0;
// 
//  	for(int i = 0; i < size; i++)
//  	{
//  		for(int j = 0; j < size; j++)
//  		{
//  			temp = 0.0;
//  			for(int k = 0; k < size; k++)
//  			{
//  				temp += A[i*size + k]*res[k*size + j];
//  			}
//  			if(i == j)
//  			{
//  				temp -= 1.0;
//  			}
//  			result += temp * temp;
//  		}
//  	}
// 
//  	return sqrt(result);
//  }

 double residual(int size, double *A, double *res)
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
 
