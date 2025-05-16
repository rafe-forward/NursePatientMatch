from .strategy_base import SolutionStrategy
from solvers.automulti_solver import AutoMultiPatientSolver

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
    def __init__(self, nurses, patients):
        self.nurses = nurses
        self.patients = patients

    def solve(self):
        solver = AutoMultiPatientSolver(self.nurses, self.patients)
        return solver.match()
