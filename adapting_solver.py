from argparse import ArgumentParser
from datetime import datetime
from math import ceil
from pathlib import Path
from sys import argv, stderr
from time import time
from typing import TextIO
from genetic_algorithm import genetic_algorithm, Individual
from genetic_algorithm.selection import TournamentSelection
from mwcnf_parser import parse_mwcnf, WeightedCnf
from solver import MwcnfGenerator
from solver.fitness import satisfied_clause_count, weights
from solver.mwcnf_individual import MwcnfIndividual

def solve_formula(formula: WeightedCnf, debug_stream: TextIO | None = None) -> tuple[Individual, int, int]:
    pop_size = ceil(max(75, 150 * (1.1041 ** (formula.variable_cnt - 36))))
    tournament_size = 1.2 * (1.02988 ** (pop_size / 150))
    return genetic_algorithm(MwcnfGenerator(formula),
                             population_size=pop_size,
                             number_of_generations=500,
                             selection=TournamentSelection(tournament_size),
                             crossover_probability=0.9,
                             mutation_rate=0.012,
                             elitism=1,
                             debug_stream=debug_stream,
                             terminate_on_stagnation_in_x_generations=0.999999,  # This is to activate last_improvement
                             )

def main():
    parser = ArgumentParser()
    parser.add_argument("--formula_file")
    parser.add_argument("--debug_to_stderr",
                        action="store_true",
                        default=False)
    args = parser.parse_args(argv[1:])

    formula_path = Path(args.formula_file)
    formula = parse_mwcnf(formula_path)
    start = datetime.now()
    solution, i, last_improvement = solve_formula(formula, stderr if args.debug_to_stderr else None)
    end = datetime.now()

    if isinstance(solution, MwcnfIndividual):
        print(f"Took {end - start}")
        print(f"Number of generations: {i + 1}. Last improvement: {last_improvement + 1}.")
        print(f"Number satisfied: {-satisfied_clause_count(formula, solution.config)}")
        print(f"{formula_path.name} {-weights(formula, solution.config)} {solution.config.get_evaluation()} 0")

if __name__ == '__main__':
    main()
