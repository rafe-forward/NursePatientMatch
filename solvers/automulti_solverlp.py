from ortools.linear_solver import pywraplp
from tools.score_calculator import calculate_score

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
class AutoMultiPatientSolverLP:
    def __init__(self, nurses, patients):
        self.nurses = nurses
        self.patients = patients

    def match(self):
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            raise Exception("SCIP solver is not available")

        n = len(self.nurses)
        m = len(self.patients)

        x = {}
        score_matrix = {}
        valid_pairs = []

        # Precompute score and valid assignment pairs
        for i in range(n):
            nurse = self.nurses[i]
            for j in range(m):
                patient = self.patients[j]
                if (
                    patient.required_shift in nurse.available_shifts
                    and patient.condition in nurse.skills
                ):
                    score = calculate_score(nurse, patient)
                    x[i, j] = solver.IntVar(0, 1, f"x[{i},{j}]")
                    score_matrix[i, j] = score
                    valid_pairs.append((i, j))

        # Enforce: Each patient assigned to exactly one nurse
        for j in range(m):
            valid_for_j = [x[i, j] for i in range(n) if (i, j) in x]
            # if not valid_for_j:
            #     raise Exception(f"No valid nurses available for patient {self.patients[j].id}")
            solver.Add(solver.Sum(valid_for_j) <= 1)
        # Enforce: Nurse can only have one patient per shift
        for i in range(n):
            nurse = self.nurses[i]
            for shift in nurse.available_shifts:
                patients_for_shift = [j for j in range(m)
                                    if (i, j) in x and self.patients[j].required_shift == shift]
                if patients_for_shift:
                    solver.Add(solver.Sum(x[i, j] for j in patients_for_shift) <= 1)
        # Enforce: Each nurse can't exceed max_patients
        for i in range(n):
            assigned = [x[i, j] for j in range(m) if (i, j) in x]
            if assigned:
                solver.Add(solver.Sum(assigned) <= self.nurses[i].max_patients)

        # Enforce: Total stress for each nurse must be ≤ 10
        for i in range(n):
            assigned = [x[i, j] for j in range(m) if (i, j) in x]
            total_stress = self.nurses[i].current_stress + 2 * solver.Sum(assigned)
            solver.Add(total_stress <= 10)

        # Objective: maximize total compatibility score
        objective = solver.Objective()
        for (i, j) in valid_pairs:
            objective.SetCoefficient(x[i, j], score_matrix[i, j])
        objective.SetMaximization()

        # Solve
        status = solver.Solve()
        print(f"Iterations: {solver.iterations()}")
        print(f"Variable count: {len(solver.variables())}")
        assignments = []
        if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
            for (i, j) in valid_pairs:
                if x[i, j].solution_value() > 0.5:
                    nurse = self.nurses[i]
                    patient = self.patients[j]
                    score = score_matrix[i, j]
                    assignments.append((nurse, patient, score))
        else:
            print("No feasible solution found.")
    
        extra_patients = []
        assigned_patient_ids = {assignment[1].id for assignment in assignments}
        for patient in self.patients:
            if patient.id not in assigned_patient_ids:
                extra_patients.append(patient)
        return (assignments,extra_patients)
