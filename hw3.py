from threading import Lock
from threading import Thread

N = 100

lock_odd = Lock()
lock_even = Lock()

lock_odd.acquire()
lock_even.acquire()


def even():
    for i in range(1, N, 2):
        lock_even.acquire()
        try:
            print('{} '.format(i))
        finally:
            lock_odd.release()


def odd():
    for i in range(0, N + 1, 2):
        lock_odd.acquire()
        try:
            print('{} '.format(i))
        finally:
            lock_even.release()


if __name__ == "__main__":
    thread_odd = Thread(target=odd)
    thread_even = Thread(target=even)

    thread_odd.start()
    thread_even.start()

    lock_odd.release()  # 0 is odd and must be first!

    thread_odd.join()  # 100 is odd too and is last!
