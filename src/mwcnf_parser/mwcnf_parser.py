from pathlib import Path
from weighted_formula import WeightedCnf, clause3_t


def parse_mwcnf(file: Path) -> WeightedCnf:
    has_seen_p_line = False
    declared_clause_cnt = None
    declared_variable_cnt = None
    weights_list = []
    clauses = []
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip()

            if line[0].lower() == 'c':
                # Ignore coments.
                continue
            elif line[0].lower() == 'p':
                line = line.split()
                assert line[1] == 'mwcnf', "The mwcnf is currently only supported format."
                declared_variable_cnt = int(line[2])
                declared_clause_cnt = int(line[3])
                has_seen_p_line = True
            elif line[0].lower() == 'w':
                weights_list = _parse_weights_line(line)
            else:
                clause = _parse_clause(line)
                clauses.append(clause)

    assert has_seen_p_line
    assert declared_clause_cnt == len(clauses)
    assert declared_variable_cnt == len(weights_list)
    
    return WeightedCnf(clauses, tuple(weights_list))


def _parse_weights_line(weigths_line: str) -> list[int]:
    weigths = weigths_line.split()
    assert weigths[0].lower() == 'w', "The argument weigths_line is not a weight line."
    assert int(weigths[-1]) == 0, "The argument weigths_line is not a weight line."
    
    weigths = weigths[1:-1]  # Remove starting 'w' and final '0'
    weigths = [int(weigth) for weigth in weigths]

    return weigths


def _parse_clause(line: str) -> clause3_t:
    clause = line.split()
    assert int(clause[-1]) == 0, "The line is not a clause in mwcnf format."

    clause = clause[:-1]  # Remove a final '0'.
    assert len(clause) == 3, "The formula is not in 3SAT format."

    return int(clause[0]), int(clause[1]), int(clause[2])
