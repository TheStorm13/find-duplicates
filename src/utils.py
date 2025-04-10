import multiprocessing as mp

import psutil


def get_optimized_thread_count():
    cpu_count = mp.cpu_count()
    # Если загрузка процессора высокая, уменьшаем количество потоков
    if psutil.cpu_percent(interval=0.1) > 75:
        return max(1, cpu_count // 2)
    return cpu_count + 4
