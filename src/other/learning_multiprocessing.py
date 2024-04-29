# *What's the difference between threading and multiprocessing?*

# Multiprocessing helps us speed up our program from multiple tasks running in parallel.

import multiprocessing
import concurrent.futures
import time


def do_something(seconds):
    print(f'Sleeping {seconds} second(s)')
    time.sleep(seconds)
    return f'done sleeping...{seconds}'


if __name__ == '__main__':
    start = time.perf_counter()

    # Basic Example
    # -----
    # p1 = multiprocessing.Process(target=do_something)
    # p2 = multiprocessing.Process(target=do_something)
    #
    # p1.start()
    # p2.start()
    #
    # p1.join()
    # p2.join()
    # -----

    # with for loops
    # processes = []
    # for _ in range(10):
    #     p = multiprocessing.Process(target=do_something, args=[2])
    #     p.start()
    #     processes.append(p)
    #
    # for process in processes:
    #     process.join()

    # --- Adding Arguments ---
    # arguments need to be able to be serialized with pickle.
    # -> arguments need to be passed into a format that can be deconstructed and reconstructed.

    # with pooling
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # If we want to use the function one at a time, we can use the submit method.
        # This schedules a function to be executed and returns a future object.

        # basic code
        # -----
        # f1 = executor.submit(do_something, 1)
        # print(f1.result())
        # -----

        # -----
        # secs = [5, 4, 3, 2, 1]
        # results = [executor.submit(do_something, sec) for sec in secs]
        #
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())
        # -----

        secs = [5, 4, 3, 2, 1]
        results = executor.map(do_something, secs)

        # for result in results:
        #     print(result)

    finish = time.perf_counter()

    print(f'Time elapsed: {round(finish - start, 2)}s')


from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        p.join()

        print(d)
        print(l)