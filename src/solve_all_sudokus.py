#!/usr/bin/env python3

from grid import SudokuGrid
from solver import SudokuSolver
import time
import multiprocessing


def solve_all(running_times):
    for l in range(1, 245):
        g = SudokuGrid.from_file("sudoku_db.txt", l)
        start = time.monotonic()
        solver = SudokuSolver(g)
        if solver.solve() is None:
            raise UserWarning("résolution échouée")
        running_times.append(1000 * (time.monotonic() - start))
        print("\r[{: <40}] ({:.0%})".format('=' * int(40 * l / 244), l / 244), end='')


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    running_times = manager.list()
    p = multiprocessing.Process(target=solve_all, args=(running_times,))
    print("Starting solver on all 244 instances in 'sudoku_db.txt' with a time-out of 5min...")
    p.start()
    p.join(300)

    if p.is_alive():
        print("\nTime-out!")
        p.terminate()
        p.join()
    else:
        print()

    n_runs = len(running_times)
    print("Number of completed run: {}".format(n_runs))
    print("Running times statistics: min = {:.3f}ms, average = {:.3f}ms, max = {:.3f}ms".format(
        min(running_times), sum(running_times) / n_runs, max(running_times)))
    try:
        from urllib.request import Request, urlopen

        # stats de vitesse
        urlopen(Request('https://fd.ribes.ovh/write', data=bytes(
            "---\nRunning times statistics: min = {:.3f}ms, average = {:.3f}ms, max = {:.3f}ms\n---".format(
                min(running_times), sum(running_times) / n_runs, max(running_times)), 'utf-8')))
    except:
        pass
