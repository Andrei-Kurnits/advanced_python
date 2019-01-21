from multiprocessing import current_process
from multiprocessing import freeze_support
from multiprocessing import Process


def printer(i, N):
    if i <= N:
        print('{} {}'.format(current_process().name, i))
        i += 1
        if i % 2:
            new_process_name = 'even'
        else:
            new_process_name = 'odd '
        Process(name=new_process_name, target=printer, args=(i, N)).start()


if __name__ == '__main__':
    freeze_support()
    p = Process(name='odd ', target=printer, args=(0, 100))
    p.start()
