from tools.score_calculator import calculate_score
from ortools.sat.python import cp_model
"""
Matching service for the patient solver
Sets constraints:
    Required shift must be in available_shifts
    Match of 1 nurse to patient
    Nurse must not get assigned no more than max_patients
    total stress must be less than nurse stress
Coefficients
    stress penalty
    score
Vars 
    score
        Calculated score from tools/store_calculator
        Involves stress level, skills matchup, scheduling
    
Output match
    (Nurse,Patient,Score)
    Nurse Object
        Defined in nurse_patient_class
    Patient Object
        Defined in nurse_patient_class
    Score
        Calculated Nurse Patient compatibility score
"""
class AutoMultiPatientSolverCP:
    def __init__(self, nurses, patients):
        self.nurses = nurses
        self.patients = patients

    def match(self):
        model = cp_model.CpModel()
        if not model:
            raise Exception("model is not available")

        n = len(self.nurses)
        m = len(self.patients)

        x = {}
        score_matrix = {}
        valid_pairs = []
        for i in range(n):
            nurse = self.nurses[i]
            for j in range(m):
                patient = self.patients[j]
                if patient.required_shift in nurse.available_shifts and patient.condition in nurse.skills:
                    var = model.NewBoolVar(f"x[{i},{j}]")
                    x[i,j] = var
                    score = calculate_score(nurse,patient)
                    score_matrix[i,j] = score
                    valid_pairs.append((i,j))
        # Constraint: Each patient must be assigned to exactly one nurse

        for j in range(m):
            valid_for_j = [x[i,j] for i in range(n) if (i,j) in x]
            if not valid_for_j:
                raise Exception(f"No valid nurses for patient {self.patients[j].id}")
            model.Add(sum(valid_for_j) == 1)
        # Constraint: Nurse can only take 1 patient per shift
        for i in range(n):
            nurse = self.nurses[i]
            for shift in nurse.available_shifts:
                patients_for_shift = [
                    j for j in range(m)
                    if (i,j) in x and self.patients[j].required_shift == shift
                ]
                if patients_for_shift:
                    model.Add(sum(x[i,j] for j in patients_for_shift) <= 1)
        # Constraint: Each nurse can't exceed their max_patient
        for i in range(n):
            assigned = [x[i,j] for j in range(m) if (i,j) in x]
            if assigned:
                model.Add(sum(assigned) <= self.nurses[i].max_patients)
        
        # Constraint: currnet + 2 per patients <= 10
        for i in range(n):
            assigned = [x[i,j] for j in range(m) if (i,j) in x]
            total_stress_expr = 2 * sum(assigned) + self.nurses[i].current_stress
            model.Add(total_stress_expr <= 10)
        model.Maximize(sum(x[i,j] * score_matrix[i,j] for (i,j) in valid_pairs))

        solver = cp_model.CpSolver()


        # Solve
        status = solver.Solve(model)
        assignments = []
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            for (i, j) in valid_pairs:
                if solver.Value(x[i, j]) == 1:
                    nurse = self.nurses[i]
                    patient = self.patients[j]
                    score = score_matrix[i, j]
                    assignments.append((nurse, patient, score))
        else:
            print("No feasible solution found.")
        return assignments
