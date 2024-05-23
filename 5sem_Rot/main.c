#include <time.h>
#include <stdlib.h>
#include "func.h"

int main(int argc, char *argv[argc]) //argv содержит от 3-х до 4-х элементов
{
//========================================================================
    int size; // размер матрицы
    int numout; // кол-во выводимых элементов
    double EPS; // машинный эпсилон

    double inv1; 
    double inv2; 
    int iter; 

    int mode; // режим ввода
    clock_t time; // время работы
    FILE *input; // файл input'а

    double *A = NULL; // матрица A
    double *val = NULL; // матрица свободных членов
//========================================================================
    if(argc < 5)
    {
        printf("\n---ОШИБКА: Недостаночно аргументов командной строки---\n");
        return EROUT;
    }

    size = atoi(argv[1]);
    numout = atoi(argv[2]);
    EPS = strtod(argv[3], NULL);
    mode = atoi(argv[4]);

    // printf("size = %d\n", size);
    // printf("numout = %d\n", numout);
    // printf("EPS = %e\n",EPS);
    // printf("mode = %d\n", mode);
//========================================================================
    if(size < 1)
    {
        printf("\n---ОШИБКА: Некоректный размер матрицы---\n");
        return EROUT;
    }
    
    if((numout < 0) || (numout > size))
    {
        printf("\n---ОШИБКА: Некоректный режим вывода элементов матрицы---\n");
        return EROUT;
    }

    if((mode != 0)&&(mode != 1)&&(mode != 2)&&(mode != 3)&&(mode != 4))
    {
        printf("\n---ОШИБКА: Некоректный режим ввода элементов матрицы---\n");
        return EROUT;
    }

    A = malloc(size * size * sizeof(double));
    val = malloc(size * sizeof(double));
//========================================================================
    if(mode == 0)
    {
        if(argc != 6)
        {
            printf("\n---ОШИБКА: Неверное кол-во аргументов командной строки---\n");
            return EROUT;
        }

        if ((input = fopen(argv[5], "r")) == NULL)
        {
            printf("\n---ОШИБКА: Проблема с открытием файла---\n");
            fclose(input);
            return EROUT;
        }

        if(fmatin(size, A, input))
        {
            printf("\n---ОШИБКА: Неверный формат ввода---\n");
            fclose(input);
            free(A);// check
            return EROUT;
        }
        fclose(input);
        printf("\n---ДИАГОСТИКА: Считывание из файла---\n");
    }else{
        if(argc != 5)
        {
            printf("\n---ОШИБКА: Неверное кол-во аргументов командной строки---\n");
            return EROUT;
        }
        generateMatrix(size, mode, A); // переделать
        printf("\n---ДИАГОСТИКА: Генерация матрицы по формуле---\n");
    }
//========================================================================    
    printf("\n---ДИАГОСТИКА: Вывод матрицы A %ld---\n", sizeof(A));
    fmatout(numout, size, A, stdout);

    inv1 = 0.0;
    inv2 = 0.0;
    for (int i = 0; i < size; ++i)
    {
        inv1 += A[i * size + i];
        for (int j = 0; j < size; ++j)
            inv2 += A[i * size + j] * A[j * size + i];
            // printf("%lf   ",inv2);
    }
    //inv2 = sqrt(inv2);

    time = clock();
    EigenVal(size, A, val, EPS, &iter);
    time = clock() - time;

    for (int i = 0; i < size; ++i)
    {
        inv1 -= val[i];
        // printf("%lf - %lf ^2 =", inv2, val[i]);
        inv2 -= val[i] * val[i];
        // printf("%lf\n",inv2);

    }
    printf("\n---ДИАГОСТИКА: Вывод матрицы A %ld---\n", sizeof(A));
    fmatout(numout, size, A, stdout);

    printf("\n---ДИАГОСТИКА: Вывод собственных значений---\n");
    fvectout(size, val, stdout);
    printf("\n");

    printf("\n---ДИАГОСТИКА: время работы алгоритма: %ld ---\n", time);
    //printf("\n---ДИАГОСТИКА: сколько итераций: %d ---\n", iter);

    printf("\n---ДИАГОСТИКА: Невязка в первом инварианте: %10.3e ---\n", fabs(inv1));
    printf("\n---ДИАГОСТИКА: Невязка во втором инварианте: %10.3e ---\n", fabs(inv2));
    
//========================================================================   
    free(A);
    free(val);

    return 0;
}
