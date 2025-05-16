#Single Solver class
"""
    init variables:
        nurses
            -list of nurse objects
        patient
            -single patient object
        return limit
            -int specifies amount to be returned from search
    return format:
        list of nurse objects sorted by score
"""
class SingleScheduleSolver():
    def __init__(self,nurses,patient, return_limit):
        self.nurses = nurses
        self.patient = patient
        self.return_limit = return_limit
    #Specific score calculation for single patients, otherwise can import from tools
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
    #
    def match(self):
        nurse_scores = [(nurse, self.score(nurse,self.patient)) for nurse in self.nurses]
        nurse_scores.sort(key=lambda x: x[1], reverse= True)
        if self.return_limit > len(nurse_scores):
            print(f"Not enough nurses for return_limit, returning first {len(nurse_scores)} nurses")
            return nurse_scores
        return nurse_scores[:self.return_limit]