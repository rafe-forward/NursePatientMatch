from abc import ABC, abstractmethod

class SolutionStrategy(ABC):
    @abstractmethod
    def solve(self):
        pass

class SinglePatientSolution(SolutionStrategy):
    def __init__(self,nurses, patient, return_limit=10):
        self.nurses = nurses
        self.patient = patient
        self.return_limit = return_limit
    def solve(self):
        solver = SingleScheduleSolver(self.nurses,self.patient,self.return_limit)
        return solver.match()

class SingleScheduleSolver():
    def __init__(self,nurses,patient, return_limit):
        self.nurses = nurses
        self.patient = patient
        self.return_limit = return_limit
    def score(self,nurse,patient):
        score = 50

        stress_score = (nurse.current_stress ** 2) / 2
        score -= stress_score

        if nurse.id in patient.preferred_nurse_ids:
            score += 20

        if patient.condition in nurse.skills:
            score += 20

        if patient.required_shift in nurse.available_shifts:
            score += 20
        else:
            score -= 40
        return max(score, 0.1)
    def match(self):
        nurse_scores = [(nurse, self.score(nurse,self.patient)) for nurse in self.nurses]
        nurse_scores.sort(key=lambda x: x[1], reverse= True)
        if self.return_limit > len(nurse_scores):
            print(f"Not enough nurses for return_limit, returning first {len(nurse_scores)} nurses")
            return nurse_scores
        return nurse_scores[:self.return_limit]
