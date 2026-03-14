import multiprocessing
from engine.worker import Worker


def start_workers(count=4):
    """
    Start multiple worker processes
    """

    workers = []

    for _ in range(count):
        worker = Worker()

        process = multiprocessing.Process(
            target=worker.run
        )

        process.start()
        workers.append(process)

    for process in workers:
        process.join()