from strategy_base import SolutionStrategy
from solvers.automulti_solver import AutoMultiPatientSolver

class AutoMultiPatientSolution(SolutionStrategy):
    def __init__(self,nurses, patients):
        self.nurses = nurses
        self.patients = patients
    def solve(self):
        solver = AutoMultiPatientSolver(self.nurses,self.patients)
        return solver.match()
