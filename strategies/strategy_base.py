from abc import ABC, abstractmethod
class SolutionStrategy(ABC):
    @abstractmethod
    def solve(self):
        pass