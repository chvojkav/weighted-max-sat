from argparse import ArgumentParser
from pathlib import Path
from sys import argv, stderr
from genetic_algorithm import genetic_algorithm
from genetic_algorithm.selection import TournamentSelection
from mwcnf_parser import parse_mwcnf
from solver import MwcnfGenerator

def main():
    parser = ArgumentParser()
    parser.add_argument("--formula_file")
    args = parser.parse_args(argv[1:])

    formula = parse_mwcnf(Path(args.formula_file))
    solution = genetic_algorithm(MwcnfGenerator(formula),
                                 population_size=50,
                                 number_of_generations=100,
                                 debug_stream=stderr,
                                 selection=TournamentSelection(3))

    print(f"{solution=}")

if __name__ == '__main__':
    main()
