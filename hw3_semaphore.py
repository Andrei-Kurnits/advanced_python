from threading import Semaphore
from threading import Thread

N = 100

sem_odd = Semaphore()
sem_even = Semaphore()

sem_odd.acquire()
sem_even.acquire()


def even():
    for i in range(1, N, 2):
        sem_even.acquire()
        try:
            print('{} '.format(i))
        finally:
            sem_odd.release()


def odd():
    for i in range(0, N + 1, 2):
        sem_odd.acquire()
        try:
            print('{} '.format(i))
        finally:
            sem_even.release()


if __name__ == "__main__":
    thread_odd = Thread(target=odd)
    thread_even = Thread(target=even)

    thread_odd.start()
    thread_even.start()

    sem_odd.release()  # 0 is odd and must be first!

    thread_odd.join()  # 100 is odd too and is last!
