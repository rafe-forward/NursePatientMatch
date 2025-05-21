from .strategy_base import SolutionStrategy
from solvers.automulti_solverlp import AutoMultiPatientSolverLP
from solvers.automulti_solvecp import AutoMultiPatientSolverCP
"""
    Solution Strategy for AutoMulti
    AutoMulti uses OR tools to match patients to nurses by score

    Init vars:
        nurses:
            list of nurse objects
        patients:
            list of patient objects
    Output solve():
        (Nurse,Patient,Score)
        Nurse Object
            #Defined in nurse_patient_class
        Patient Object
            #Defined in nurse_patient_class
        Score
            #Calculated Nurse Patient compatibility score

"""


class AutoMultiPatientSolution(SolutionStrategy):
    def __init__(self, nurses, patients, strat):
        self.nurses = nurses
        self.patients = patients
        self.strat = strat
    def solve(self):
        if self.strat == "lp":
            solver = AutoMultiPatientSolverLP(self.nurses, self.patients)
            return solver.match()
        elif self.strat == "cp":
            solver = AutoMultiPatientSolverCP(self.nurses, self.patients)
            return solver.match()
        else:
            print("None")
        return solver.match()
