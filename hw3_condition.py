from threading import Condition
from threading import Thread

N = 100
i = -1

cond_produced = Condition()
cond_processed = Condition()


def generator():
    for x in range(0, N + 1):
        global i
        i = x
        with cond_produced:
            cond_produced.notifyAll()
        with cond_processed:
            cond_processed.wait()


def even():
    while i <= 100:
        with cond_produced:
            cond_produced.wait()
        if i % 2 != 0:
            print('{} '.format(i))
            with cond_processed:
                cond_processed.notify()


def odd():
    while i <= 100:
        with cond_produced:
            cond_produced.wait()
        if i % 2 == 0:
            print('{} '.format(i))
            with cond_processed:
                cond_processed.notify()


if __name__ == "__main__":
    thread_generator = Thread(target=generator)
    thread_even = Thread(target=even)
    thread_odd = Thread(target=odd)

    thread_odd.start()
    thread_even.start()
    thread_generator.start()

    thread_generator.join()
