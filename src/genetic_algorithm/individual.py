from functools import total_ordering

@total_ordering
class Individual:
    def fitness(self) -> int:
        raise NotImplementedError
    
    def mutate(self) -> "Individual":
        raise NotImplementedError
    
    def breed(self, other: "Individual") -> "Individual":
        raise NotImplementedError

    def __lt__(self, other: "Individual") -> bool:
        return self.fitness() < other.fitness()
    
    def __eq__(self, other: "Individual") -> bool:
        return self.fitness() == other.fitness()
