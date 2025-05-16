from abc import ABC, abstractmethod
"""
    Used Strategy Design Pattern to implement different solvers for different problems
    For example no need to use OR tools to match a single patient into the schedule

"""
class SolutionStrategy(ABC):
    @abstractmethod
    def solve(self):
        pass