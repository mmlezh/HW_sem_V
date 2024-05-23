#include <pthread.h>
#include "synchronize.h"


// Для ожидания в текущем потоке остальных потоков 
void synchronize(int total_threads)
{
	// Инициализация объекта типа mutex
	static pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

	// инициализация объекта типа condvar
	static pthread_cond_t condvar_in = PTHREAD_COND_INITIALIZER;

	// Объект инициализации типа condvar
	static pthread_cond_t condvar_out = PTHREAD_COND_INITIALIZER;
	
	// Число пришедших в функцию задач
	static int threads_in = 0;

	// Число ожидающих выхода
	static int threads_out = 0;

	// Блокировка mutex для работы с переменными
	pthread_mutex_lock(&mutex);

	// Увеличить число прибывших в эту функию задач
	threads_in++;

	// Проверка кол-ва
	if (threads_in >= total_threads)
	{
		// Текущий поток пришел последним 
		threads_out = 0;

		// разрешаем останьным продолжать работу
		pthread_cond_broadcast(&condvar_in);
	} else // Еще есть не пришедшие потоки

		// Ожидаем пока все потоки не придут
		while (threads_in < total_threads)
		{
			// Ждем разрешения продолжить работу: 
			// освободить mutex и ждать сигнала от condvar,
			// затем заблокиовать mutex опять 
			pthread_cond_wait(&condvar_in,&mutex);
		}

	// Увеличить число задач ожидаюших выхода
	threads_out++;

	// Провера числа ожидающих задач
	if (threads_out >= total_threads)
	{
		threads_in = 0;
		pthread_cond_broadcast(&condvar_out);
	} else
		while (threads_out < total_threads)
			pthread_cond_wait(&condvar_out,&mutex);

	pthread_mutex_unlock(&mutex);
}
