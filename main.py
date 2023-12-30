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
    parser.add_argument("--population_size",
                        default=200)
    parser.add_argument("--generation_cnt",
                        default=1000)
    parser.add_argument("--tournament_size",
                        default=1.75)
    parser.add_argument("--crossover_probability",
                        default=0.9)
    parser.add_argument("--mutation_rate",
                        default=0.03)
    parser.add_argument("--elitism",
                        default=1)
    args = parser.parse_args(argv[1:])

    formula_path = Path(args.formula_file)
    formula = parse_mwcnf(formula_path)
    solution = genetic_algorithm(MwcnfGenerator(formula),
                                 population_size=args.population_size,
                                 number_of_generations=args.generation_cnt,
                                 selection=TournamentSelection(args.tournament_size),
                                 crossover_probability=args.crossover_probability,
                                 mutation_rate=args.mutation_rate,
                                 elitism=args.elitism,
                                 debug_stream=stderr)

    if isinstance(solution, MwcnfIndividual):
        print(f"Number satisfied: {satisfied_clause_count(formula, solution.config)}")
        print(f"{formula_path.name} {-weights(formula, solution.config)} {solution.config.get_evaluation()} 0")

if __name__ == '__main__':
    main()
