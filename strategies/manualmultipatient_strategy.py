from strategies.single_strategy import SinglePatientSolution
from .strategy_base import SolutionStrategy
class ManualMultiPatientSolution(SolutionStrategy):
    def __init__(self, nurse_list, patient_list, return_limit=10):
        self.nurse_list = nurse_list
        self.patient_list = patient_list
        self.return_limit = return_limit

    def solve(self):
        results = []
        for patient in self.patient_list:
            sps = SinglePatientSolution(self.nurse_list, patient, self.return_limit)
            scored_nurses = sps.solve()
            results.append((patient, scored_nurses))
        return results
