#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include <pthread.h>
// Нужна для работы с потоками

#include "matrix.h"
#include "task.h"

void *inverse(void *p_arg);

typedef struct // 
{
    int size;
    double *A;
    double *res;
    int *inds;
    int my_rank;
    int total_threads;
} ARGS;

long int thread_time = 0; //+
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER; // инициализация объекта синхронизации

void *inverse(void *p_arg) // +
{
    ARGS *arg = (ARGS*)p_arg;
    long int time;

    time = get_time();
    invert(arg->size, arg->A, arg->res, arg->inds, arg->my_rank, arg->total_threads);
    time = get_time() - time;

    pthread_mutex_lock(&mutex);
    thread_time += time;
    pthread_mutex_unlock(&mutex);

    return NULL;
}


int main(int argc, char *argv[argc]) //argv содержит от 4-х до 5-х элементов
{
//========================================================================
    int size; // размер матрицы
    int numout; // кол-во выводимых элементов
    int mode; // режим ввода
    // clock_t time;
    FILE *input; // файл input'а

    //int result;

    double *A = NULL; // матрица A
    int *inds = NULL; // индексы
    double *res = NULL; // матрица свободных членов

    // double resid;

    long int t_full; // полное время
    int total_threads; // число потоков
    pthread_t *threads; // индексы потоков
    ARGS *args; 
    // MULDATA *mul_args;

//========================================================================
    if(argc < 5)
    {
        printf("\n---ОШИБКА: Недостаночно аргументов командной строки---\n");
        return EROUT;
    }

    total_threads = atoi(argv[1]);
    size = atoi(argv[2]);
    numout = atoi(argv[3]);
    mode = atoi(argv[4]);
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

    A = (double*)malloc(size * size * sizeof(double));
    inds = (int*)malloc(size * sizeof(double));
    res = (double*)malloc(size * size* sizeof(double));

    threads = (pthread_t*)malloc(total_threads * sizeof(pthread_t));
    args = (ARGS*)malloc(total_threads * sizeof(ARGS));
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

        if(fmatin(size, A, inds, input))
        {
            printf("\n---ОШИБКА: Неверный формат ввода---\n");
            fclose(input);
            free(A);
            free(inds);
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
        generateMatrix(size, mode, A, inds);
        printf("\n---ДИАГОСТИКА: Генерация матрицы по формуле---\n");
    }
//========================================================================    
    printf("\n---ДИАГОСТИКА: Вывод матрицы A---\n");
    fmatout(numout, size, A, stdout);

    for(int i = 0; i < size; i++)
    {
        inds[i] = i;
    }
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

    for (int i = 0; i < total_threads; i++)
    {
        args[i].size = size;
        args[i].A = A;
        args[i].res = res;
        args[i].inds = inds;
        args[i].my_rank = i;
        args[i].total_threads = total_threads;
    }

    t_full = get_full_time();

    for (int i = 0; i < total_threads; i++)
    {
        if (pthread_create(threads + i, 0, inverse, args + i))// создание потоков
        {
            printf("\n---ДИАГОСТИКА: Невозможно создать задачу %d!---\n", i);

            if (A) free(A);
            if (res) free(res);
            if (inds) free(inds);
            if (threads) free(threads);
            if (args) free(args);

            return EROUT;
        }
    }

    for (int i = 0; i < total_threads; i++) // новая
    { 
        if (pthread_join(threads[i], 0))// ждем завершения задачи
        {
            printf("\n---ДИАГОСТИКА: Невозможно закончить задачу %d!---\n", i);

            if (A) free(A);
            if (res) free(res);
            if (inds) free(inds);
            if (threads) free(threads);
            if (args) free(args);

            return EROUT;
        }
    }

    t_full = get_full_time() - t_full;

    if (t_full == 0) // очень быстрый компьютер
    {
        t_full = 1;
    }

    printf("\n---ДИАГОСТИКА: Вывод матрицы A^{-1}---\n");
    fmatout(numout, size, res, stdout);
    
    // printf("\n---ДИАГОСТИКА: Затраченное время = %ld\nОбщее время выполнения задач = %ld (%ld%%)\nВ среднем на задачу = %ld\n", t_full, thread_time, thread_time * 100/t_full, thread_time/total_threads);

//     printf("\n---ДИАГОСТИКА: Затраченное время = %ld--\n--Общее время выполнения задач = %ld--",(double)t_full/CLOCKS_PER_SEC, (double)thread_time/CLOCKS_PER_SEC);
    printf("\n---ДИАГОСТИКА: Затраченное время = %ld--\n--Общее время выполнения задач = %ld--",t_full, thread_time);
    // printf("\n---ДИАГОСТИКА: Затраченное время = %ld--",  t_full);

    // printf("\n---ДИАГОСТИКА: время работы алгоритма: %ld ---\n", time);

//========================================================================   
    
    if(mode == 0)
    {
        if ((input = fopen(argv[5], "r")) == NULL)
        {
            printf("\n---ОШИБКА: Проблема с открытием файла 2---\n");
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
    free(threads);
    free(args);

    return 0;
}
