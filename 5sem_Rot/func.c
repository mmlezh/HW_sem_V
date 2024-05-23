#include "func.h"

//==============================================//

int fmatin(int size, double *A, FILE *input)//O(n^2)
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
			// fprintf(output, "%.2lf\t", A[j+i*size]);
		}
	}
	fprintf(output,"\n");
}

void fvectout(int size, double *v, FILE *output)
{
	fprintf(output, "\n\t");
	for(int i = 0; i < size; i++)
	{
		fprintf(output, "%10.3e\t", v[i]);
		// fprintf(output, "%.2lf\t", v[i]);
	}
	fprintf(output,"\n");
}

void generateMatrix(int size, int numout, double *A)//O(n^2)
{
	for(int i = 0; i < size; i++)
	{
		for(int j = 0; j < size; j++)
		{
			A[i*size + j] = f(i+1, j+1, numout, size);
		}
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
			if(i == j)
			{
				return 2;
			}else if (abs(i-j) == 1)
			{
				return -1;
			} else {
				return 0;
			}
		case 3:
			if((i == j)&&(j < size))
			{
				// return abs(i-j);
				return 1;
			} else if(j == size)
			{
				return i;
			}else if (i == size)
			{
				return j;
			}else
			{
				return 0;
			}
		case 4: 
			return 1.0/(i+j-1.0);
		default: 
		 	return 0;
	}
}

//==============================================//

void Rot(int size, double *A)
{
	double x;
	double y;
	double r;
	double s;
	double a_ii;
	double a_ij;
	double a_ji;
	double a_jj;
	double cosPhi;
	double sinPhi;

	for (int i = 1; i < size - 1; ++i)
	{
		for (int j = i + 1; j < size; ++j)
		{
			x = A[i * size + i - 1];
			y = A[j * size + i - 1];

			if (fabs(y) < MachineEPS) // Зачем такая точность? Заменить на EPS
				continue;

			r = sqrt(x * x + y * y); 

			if (r < MachineEPS) // Зачем такая точность? Заменить на EPS
				continue;

			cosPhi = x / r;
			sinPhi = -y / r;

			A[i * size + i - 1] = A[(i - 1) * size + i] = r;
			A[j * size + i - 1] = A[(i - 1) * size + j] = 0.0;

			for (int k = i + 1; k < size; ++k)
			{
				if (k == j)
					continue;

				x = A[i * size + k];
				y = A[j * size + k];
				A[k * size + i] = A[i * size + k] = x * cosPhi - y * sinPhi;
				A[k * size + j] = A[j * size + k] = x * sinPhi + y * cosPhi;
			}

			x = A[i * size + i];
			y = A[j * size + j];
			r = A[i * size + j];
			s = A[j * size + i];

			a_ii = x * cosPhi - s * sinPhi;
			a_ji = x * sinPhi + s * cosPhi;
			a_ij = r * cosPhi - y * sinPhi;
			a_jj = r * sinPhi + y * cosPhi;

			A[i * size + i] = a_ii * cosPhi - a_ij * sinPhi;
			A[j * size + i] = a_ii * sinPhi + a_ij * cosPhi;
			A[i * size + j] = A[j * size + i];
			A[j * size + j] = a_ji * sinPhi + a_jj * cosPhi;
		}
	}
}

double norma(int size, double *A)
{
	double result;

	result = 0.0;
	for (int i = 0; i < size; ++i)
	{
		double tmp;
		tmp = 0.0;
		for (int j = 0; j < size; ++j)
		{
			tmp += fabs(A[i * size + j]);
		}

		if (result < tmp)
		{
			result = tmp;
		}
	}

	return result;
}

int n_(int size, double *A, double l)
{
	int result;
	double x;
	double y;
	double a_k;
	double b_k1;

	x = A[0 * size + 0] - l;
	y = 1.0;
	result = x < 0.0 ? 1 : 0;

	for (int i = 1; i < size; ++i)
	{
		double tmp;
		double g;
		double u;
		double v;
		a_k = A[i * size + i] - l;
		b_k1 = A[i * size + i - 1];

		tmp = fabs(b_k1 * b_k1 * y);

		if (fabs(x) > tmp)
		{
			tmp = fabs(x);
		}

		if (tmp < MachineEPS) // Почему такая точность? 
		{
			tmp = MachineEPS; // Почему такая точность?
		}
		
		g = (1.0/MachineEPS)/tmp;

		u = g * (a_k * x - b_k1 * b_k1 * y);
		v = g * x;

		if (u * x < 0.0)
			result++;

		x = u;
		y = v;
	}

	return result;
}

// int n_(int n, double* a, double lambda)
// {
// 	int i;
// 	int rezult;
// 	double x;
// 	double y;
// 	double u;
// 	double v;
// 	double tmp;
// 	double a_k;
// 	double b_k1;
// 	double gamma;

// 	x = a[0 * n + 0] - lambda;
// 	y = 1.0;
// 	rezult = x < 0.0 ? 1 : 0;

// 	for (i = 1; i < n; ++i)
// 	{
// 		a_k = a[i * n + i] - lambda;
// 		b_k1 = a[i * n + i - 1];

// 		tmp = fabs(b_k1 * b_k1 * y);

// 		if (fabs(x) > tmp)
// 			tmp = fabs(x);

// 		if (tmp < 1e-50)
// 			tmp = 1e-15;

// 		gamma = 1e15 / tmp;
// 		u = gamma * (a_k * x - b_k1 * b_k1 * y);
// 		v = gamma * x;

// 		if (u * x < 0.0)
// 			++rezult;

// 		x = u;
// 		y = v;
// 	}

// 	return rezult;
// }


void EigenVal(int size, double *A, double *val, double EPS, int *iter)
{
	int i;
	int it;
	int count;
	
	double left;
	double right;

	double currentLeft;
	double currentRight;

	Rot(size, A);
	// printf("\nматрица после поврота\n");
	// fmatout(4, size, A, stdout);


	right = norma(size, A) + EPS; // почему?
	right = norma(size, A) + EPS; // почему?
	left = -right;

	it = 0;

	i = 0;
	currentLeft = left;
	currentRight = right;

	while (i < size)
	{
		double currentMiddle;
		while (currentRight - currentLeft > EPS)
		{
			currentMiddle = 0.5 * (currentLeft + currentRight);

			if (n_(size, A, currentMiddle) < i + 1)
				currentLeft = currentMiddle;
			else
				currentRight = currentMiddle;

			if(it > MAXIT)
			{
				break;
			}

			it++;
		}

		currentMiddle = 0.5 * (currentLeft + currentRight);
		count = n_(size, A, currentRight) - n_(size, A, currentLeft);

		for (int j = 0; j < count; ++j)
		{
			if(i + j < size)
			{
				val[i + j] = currentMiddle;
			}
		}
		i += count;

		currentLeft = currentMiddle;
		currentRight = right;
	}

	*iter = it;
}
