from strategy_base import SolutionStrategy
from solvers.single_solver import SingleScheduleSolver

class SinglePatientSolution(SolutionStrategy):
    def __init__(self,nurses, patient, return_limit=10):
        self.nurses = nurses
        self.patient = patient
        self.return_limit = return_limit
    def solve(self):
        solver = SingleScheduleSolver(self.nurses,self.patient,self.return_limit)
        return solver.match()