from functools import total_ordering

@total_ordering
class Individual:
    def fitness(self) -> float:
        """Posifive number. The less, the better."""
        raise NotImplementedError
    
    def mutate(self) -> "Individual":
        raise NotImplementedError
    
    def breed(self, other: "Individual") -> tuple["Individual", "Individual"]:
        raise NotImplementedError

    def __lt__(self, other: "Individual") -> bool:
        return self.fitness() < other.fitness()
    
    def __eq__(self, other: "Individual") -> bool:
        return self.fitness() == other.fitness()
