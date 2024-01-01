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
        solution, actual_generation_cnt = genetic_algorithm(MwcnfGenerator(formula),
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
            f.write(f"{formula_path.name},{work.run_no},{clause_cnt},{sat_clause_cnt},{weight},{work.pop_size},{work.gen_cnt},{work.tour_size},{work.cross},{work.mut}\n")


def main():
    THREAD_CNT = 50
    INSTANCES = [f"wuf36-157/wruf36-157-Q/wruf36-157-{i}.mwcnf" for i in range(1, 10)]
    TOURNAMENT_SIZES = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]
    CROSSOVERS = [0.1, 0.35, 0.5, 0.65, 0.9]
    MUTATIONS = [0.005, 0.008, 0.01, 0.012, 0.015]
    STATS_FILE = "out/stats.csv"
    RUN_COUNT = 50

    Path("out").mkdir()

    work_queue = Queue()

    for instance, tour, cross, mut, run_no in product(INSTANCES, TOURNAMENT_SIZES, CROSSOVERS, MUTATIONS, range(RUN_COUNT)):
        work_queue.put_nowait(Work(formula=instance,
                                   run_no=run_no,
                                   pop_size=100,
                                   gen_cnt=300,
                                   tour_size=tour,
                                   cross=cross,
                                   mut=mut,
                                   debug_output_file=f"out/{Path(instance).name}-{run_no}-{tour}-{cross}-{mut}",
                                   stats_file=STATS_FILE))

    processes = [Process(target=thread_func, args=(work_queue,)) for _ in range(THREAD_CNT)]
    for process in processes:
        process.start()

    try:
        while not work_queue.empty():
            print(f"\rRemaining task count (approximate): {work_queue.qsize()}", end='')
            sleep(0.5)
    finally:
        # In case we get an exception (f.e. KeyboardInterrupt)
        while True:
            try:
                _ = work_queue.get_nowait()
            except Empty:
                break

        for process in processes:
            process.terminate()

if __name__ == '__main__':
    main()
