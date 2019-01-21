from threading import Event
from threading import Thread

N = 100

event = Event()


def even(val):
    print('Even: {} '.format(val))
    event.set()


def odd(val):
    print('Odd:  {} '.format(val))
    event.set()


if __name__ == "__main__":
    for i in range(0, N + 1):
        if i % 2 == 0:
            Thread(target=odd, args=(i,)).start()
        else:
            Thread(target=even, args=(i,)).start()
        event.wait()
