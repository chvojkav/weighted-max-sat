from argparse import ArgumentParser
from pathlib import Path
from sys import argv, stderr
from genetic_algorithm import genetic_algorithm
from genetic_algorithm.selection import TournamentSelection
from mwcnf_parser import parse_mwcnf
from solver import MwcnfGenerator
from solver.fitness import satisfied_clause_count, weights
from solver.mwcnf_individual import MwcnfIndividual

def main():
    parser = ArgumentParser()
    parser.add_argument("--formula_file")
    args = parser.parse_args(argv[1:])

    formula_path = Path(args.formula_file)
    formula = parse_mwcnf(formula_path)
    solution = genetic_algorithm(MwcnfGenerator(formula),
                                 population_size=200,
                                 number_of_generations=1000,
                                 debug_stream=stderr,
                                 selection=TournamentSelection(3),
                                 mutation_rate=0.01)

    if isinstance(solution, MwcnfIndividual):
        print(f"Number satisfied: {satisfied_clause_count(formula, solution.config)}")
        print(f"{formula_path.name} {-weights(formula, solution.config)} {solution.config.get_evaluation()} 0")

if __name__ == '__main__':
    main()
