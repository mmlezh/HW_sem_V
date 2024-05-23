#include <time.h>
#include "matrix.h"

int main(int argc, char *argv[argc]) //argv содержит от 3-х до 4-х элементов
{
//========================================================================
    int size; // размер матрицы
    int numout; // кол-во выводимых элементов
    int mode; // режим ввода
    clock_t time;
    FILE *input; // файл input'а

    //int result;

    double *A = NULL; // матрица A
    int *inds = NULL;
    double *res = NULL; // матрица свободных членов
//========================================================================
    if(argc < 4)
    {
        printf("\n---ОШИБКА: Недостаночно аргументов командной строки---\n");
        return EROUT;
    }

    size = atoi(argv[1]);
    numout = atoi(argv[2]);
    mode = atoi(argv[3]);
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
    inds = malloc(size * sizeof(double));
    res = malloc(size * size* sizeof(double));
//========================================================================
    if(mode == 0)
    {
        if(argc != 5)
        {
            printf("\n---ОШИБКА: Неверное кол-во аргументов командной строки---\n");
            return EROUT;
        }

        if ((input = fopen(argv[4], "r")) == NULL)
        {
            printf("\n---ОШИБКА: Проблема с открытием файла---\n");
            fclose(input);
            return EROUT;
        }

        if(fmatin(size, A, inds, input))
        {
            printf("\n---ОШИБКА: Неверный формат ввода---\n");
            fclose(input);
            free(A);// check
            free(inds);
            return EROUT;
        }
        fclose(input);
        printf("\n---ДИАГОСТИКА: Считывание из файла---\n");
    }else{
        if(argc != 4)
        {
            printf("\n---ОШИБКА: Неверное кол-во аргументов командной строки---\n");
            return EROUT;
        }
        generateMatrix(size, mode, A, inds);
        printf("\n---ДИАГОСТИКА: Генерация матрицы по формуле---\n");
    }
//========================================================================    
    printf("\n---ДИАГОСТИКА: Вывод матрицы A---\n");
    fmatout(numout, size, A, stdout);

    time = clock();
    if(gsolve(size, A, inds, res))
    {
        printf("Вырожденная матрица");
    }
    time = clock() - time;
    printf("\n---ДИАГОСТИКА: время работы алгоритма: %ld ---\n", time);

    //printf("\n---ДИАГОСТИКА: Вывод матрицы A после gsolve---\n");
    //fmatout(numout, size, A, stdout);

    printf("\n---ДИАГОСТИКА: Вывод матрицы A^{-1} после gsolve---\n");
    fmatout(numout, size, res, stdout);
    
//========================================================================   
    
    if(mode == 0)
    {

        if ((input = fopen(argv[4], "r")) == NULL)
        {
            printf("\n---ОШИБКА: Проблема с открытием файла---\n");
            fclose(input);
            return EROUT;
        }

        if(fmatin(size, A, inds, input))
        {
            printf("\n---ОШИБКА: Неверный формат ввода---\n");
            fclose(input);
            free(A);// check
            free(inds);
            return EROUT;
        }
        fclose(input);
    }else{
        generateMatrix(size, mode, A, inds);
    }
    
    printf("\n---ДИАГОСТИКА: Нормы невязки ||A*A^{-1}-E|| = %10.3e\t ---\n", residual(size, A, res));
    
    free(A);
    free(res);
    free(inds);

    return 0;
}
