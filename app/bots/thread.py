import time
from threading import Thread


def run_multi_process(*fns):
    for fn in fns:
        # p = Process(target=fn,)
        p = Thread(target=fn)
        p.daemon = True
        p.start()
    print('yeah process')


def run_thread_fn(fn, *args, **kwargs):
    p = Thread(target=fn,args=args, kwargs=kwargs)
    p.daemon = True
    p.start()


def test_thread(name, counter):
    print(name, counter, end="\n")
    time.sleep(2)
    print("end function, ", counter, end="\n")


if __name__ == "__main__":
    for i in range(10):
        name = f"Hello {i*i}"
        run_thread_fn(test_thread, name, i)