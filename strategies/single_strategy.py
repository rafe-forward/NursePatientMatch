from .strategy_base import SolutionStrategy
from solvers.single_solver import SingleScheduleSolver
"""
    SinglePatientSolution
    Employs single patient solver to generate the top n best matches for a patient

    init vars:
        nurses:
            list of nurse objects
        patient:
            singular patient object
        return_limit:
            amount of returns for search of nurses
    
    solve():
        uses single schedule solver to return a list of return_limit nurse objects sorted by score to patient

"""
class SinglePatientSolution(SolutionStrategy):
    def __init__(self,nurses, patient, return_limit=10):
        self.nurses = nurses
        self.patient = patient
        self.return_limit = return_limit
    def solve(self):
        solver = SingleScheduleSolver(self.nurses,self.patient,self.return_limit)
        return solver.match()