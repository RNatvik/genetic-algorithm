import threading
import time


class ReusableThread:

    def __init__(self):
        self.thread = threading.Thread(target=self._run)
        self.start_event = threading.Event()
        self.end_event = threading.Event()
        self.event_lock = threading.Lock()
        self.cmd_kill = False
        self.args = []
        self.kwargs = {}
        self.func = None
        self.available = True

        self.thread.start()

    def start(self, func, args=None, kwargs=None):
        result = False
        if self.available:
            self.available = False
            self.args = args if args is not None else []
            self.kwargs = kwargs if kwargs is not None else {}
            self.func = func
            with self.event_lock:
                self.start_event.set()
                self.end_event.clear()
            result = True
        return result

    def _run(self):
        while not self.cmd_kill:
            start = self.start_event.wait()
            if start and not self.cmd_kill:
                self.func(*self.args, **self.kwargs)
                with self.event_lock:
                    self.start_event.clear()
                    self.end_event.set()
                self.available = True

    def kill(self):
        self.cmd_kill = True
        self.start_event.set()


class PoolThread(ReusableThread):

    def __init__(self, queue: list, lock: threading.Lock):
        super().__init__()
        self.queue = queue
        self.lock = lock

    def _run(self):
        while not self.cmd_kill:
            start = self.start_event.wait()
            if start and not self.cmd_kill:
                self.func(*self.args, **self.kwargs)
                with self.event_lock:
                    self.start_event.clear()
                    self.end_event.set()
                self.available = True

                task = None
                with self.lock:
                    if len(self.queue) > 0:
                        task = self.queue.pop(0)
                if task is not None:
                    self.start(task[0], task[1], task[2])


class ThreadPool:

    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.queue = []
        self.queue_lock = threading.Lock()
        self.shutdown = False

        self.pool = self._generate_pool()

        self.add_times = {}
        self.execute_times = {}
        self.monitor_times = {}

    def add_task(self, function, args=None, kwargs=None):
        assigned = False
        self.add_times[args[0]] = time.time()
        with self.queue_lock:
            for thread in self.pool:
                if thread.available:
                    print(f'Immediate start: {args}')
                    thread.start(function, args=args, kwargs=kwargs)
                    assigned = True
                    break
            if not assigned:
                print(f'Queued start: {args}')
                task = (function, args, kwargs)
                self.queue.append(task)

    def stop(self):
        self.shutdown = True
        for thread in self.pool:
            thread.kill()

    def _generate_pool(self):
        threads = []
        for i in range(self.pool_size):
            thread = PoolThread(self.queue, self.queue_lock)
            threads.append(thread)
        return threads


def task_(a):
    te = time.time()
    print(f'{a}: enter - {te}')
    time.sleep(1)
    te = time.time()
    print(f'{a}: exit - {te}')


def main():
    n = 5
    pool = ThreadPool(n)
    for i in range(n+2):
        pool.add_task(task_, args=[i])
    time.sleep(5)
    pool.stop()
    time.sleep(3)
    for key in pool.add_times.keys():
        print(f'Add: {key} - {pool.add_times[key]}')


if __name__ == '__main__':
    main()
