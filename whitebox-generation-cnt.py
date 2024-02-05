from itertools import product
from pathlib import Path
from multiprocessing import Queue, Process
from queue import Empty
from time import sleep
from genetic_algorithm import genetic_algorithm
from genetic_algorithm.selection import TournamentSelection
from mwcnf_parser import parse_mwcnf
from solver import MwcnfGenerator
from solver.fitness import satisfied_clause_count, weights

from io import StringIO
from dataclasses import dataclass


@dataclass
class Work:
    formula: str
    run_no: int
    pop_size: int
    gen_cnt: int
    tour_size: float
    cross: float
    mut: float
    debug_output_file: str
    stats_file: str

def thread_func(work_queue: Queue):
    while not work_queue.empty():
        try:
            work = work_queue.get_nowait()
        except Empty:
            break

        debug_stream = StringIO()
        formula_path = Path(work.formula)
        formula = parse_mwcnf(formula_path)
        solution, _, last_improvement  = genetic_algorithm(MwcnfGenerator(formula),
                                                            population_size=work.pop_size,
                                                            number_of_generations=work.gen_cnt,
                                                            selection=TournamentSelection(work.tour_size),
                                                            crossover_probability=work.cross,
                                                            mutation_rate=work.mut,
                                                            elitism=1,
                                                            debug_stream=debug_stream)

        with open(Path(work.debug_output_file), mode="wt+") as f:
            f.write(debug_stream.getvalue())

        with open(work.stats_file, mode="at+") as f:
            clause_cnt = formula.clause_cnt
            sat_clause_cnt = -satisfied_clause_count(formula, solution.config)
            weight = -weights(formula, solution.config)
            f.write(f"{formula_path.name},{work.run_no},{clause_cnt},{sat_clause_cnt},{weight},{last_improvement},{work.pop_size}\n")


def main():
    THREAD_CNT = 24
    INSTANCES = [f"wuf50-218/wuf50-218-Q/wuf50-0{i}.mwcnf" for i in range(1, 11)]
    POPULATIONS = [600]
    STATS_FILE = "out/stats.csv"
    RUN_COUNT = 10
    Path("out").mkdir()

    work_queue = Queue()

    for pop_size, instance, run_no in product(POPULATIONS, INSTANCES, range(RUN_COUNT)):
        work_queue.put_nowait(Work(formula=instance,
                                   run_no=run_no,
                                   pop_size=pop_size,
                                   gen_cnt=500,
                                   tour_size=1.4,
                                   cross=0.9,
                                   mut=0.012,
                                   debug_output_file=f"out/{Path(instance).name}-{pop_size}-{run_no}",
                                   stats_file=STATS_FILE))

    processes = [Process(target=thread_func, args=(work_queue,)) for _ in range(THREAD_CNT)]
    for process in processes:
        process.start()

    try:
        while not work_queue.empty():
            print(f"\rRemaining task count (approximate): {work_queue.qsize()}", end='')
            sleep(0.5)
    finally:
        print("\nTerminating...")
        # In case we get an exception (f.e. KeyboardInterrupt)
        while True:
            try:
                _ = work_queue.get_nowait()
            except Empty:
                break

        sleep(3)

        for process in processes:
            process.terminate()

if __name__ == '__main__':
    main()
