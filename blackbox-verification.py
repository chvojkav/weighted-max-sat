from itertools import product
from pathlib import Path
from multiprocessing import Queue, Process
from queue import Empty
from time import sleep
from mwcnf_parser import parse_mwcnf
from solver.fitness import satisfied_clause_count, weights

from dataclasses import dataclass

import sys
sys.path.append(str(Path.cwd()))
from adapting_solver import solve_formula

@dataclass
class Work:
    formula: str
    run_no: int
    stats_file: str

def thread_func(work_queue: Queue):
    while not work_queue.empty():
        try:
            work = work_queue.get_nowait()
        except Empty:
            break

        formula_path = Path(work.formula)
        formula = parse_mwcnf(formula_path)
        solution, _, last_improvement  = solve_formula(formula)

        with open(work.stats_file, mode="at+") as f:
            clause_cnt = formula.clause_cnt
            sat_clause_cnt = -satisfied_clause_count(formula, solution.config)
            weight = -weights(formula, solution.config)
            f.write(f"{formula_path.name},{work.run_no},{clause_cnt},{sat_clause_cnt},{weight},{last_improvement}\n")


def main():
    THREAD_CNT = 24
    INSTANCES = [f"wuf50-218/wuf50-218-Q/wuf50-0{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf50-218/wuf50-218-M/wuf50-0{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf50-218/wuf50-218-N/wuf50-0{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf50-218/wuf50-218-R/wuf50-0{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf36-157/wruf36-157-M/wruf36-157-{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf36-157/wruf36-157-N/wruf36-157-{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf36-157/wruf36-157-Q/wruf36-157-{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf36-157/wruf36-157-R/wruf36-157-{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf20-91/wuf20-91-M/wuf20-0{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf20-91/wuf20-91-N/wuf20-0{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf20-91/wuf20-91-Q/wuf20-0{i}.mwcnf" for i in range(67, 77)] + \
        [f"wuf20-91/wuf20-91-R/wuf20-0{i}.mwcnf" for i in range(67, 77)]
    STATS_FILE = "blackbox-out/stats.csv"
    RUN_COUNT = 10
    Path("blackbox-out").mkdir()

    work_queue = Queue()

    for instance, run_no in product(INSTANCES, range(RUN_COUNT)):
        work_queue.put_nowait(Work(formula=instance,
                                   run_no=run_no,
                                   stats_file=STATS_FILE))

    processes = [Process(target=thread_func, args=(work_queue,)) for _ in range(THREAD_CNT)]
    for process in processes:
        process.start()

    try:
        while not work_queue.empty():
            print(f"\rRemaining task count (approximate): {work_queue.qsize()}", end='')
            sleep(0.5)

        for process in processes:
            process.join()
    finally:
        print("\nTerminating...")
        # In case we get an exception (f.e. KeyboardInterrupt)
        while True:
            try:
                _ = work_queue.get_nowait()
            except Empty:
                break

        for process in processes:
            process.terminate()

        for process in processes:
            process.join()

if __name__ == '__main__':
    main()
