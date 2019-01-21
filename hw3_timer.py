from threading import Timer
import time

N = 100
i = 0


def even():
    global i, N
    if i <= N:
        print('{} '.format(i))
        i += 1
        Timer(0.01, odd).start()


def odd():
    global i, N
    if i <= N:
        print('{} '.format(i))
        i += 1
        Timer(0.01, even).start()


if __name__ == "__main__":
    odd()

    while i <= 100:
        time.sleep(0.1)
