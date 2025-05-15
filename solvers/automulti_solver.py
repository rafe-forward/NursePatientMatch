from scipy.optimize import linear_sum_assignment
import numpy as np
from ortools.linear_solver import pywraplp
from score_calculator import calculate_score
class AutoMultiPatientSolver():
    def __init__(self,nurses,patients):
        self.nurses = nurses
        self.patients = patients
    def match(self):
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver: 
            raise Exception("SCIP solver is not available")
        n = len(self.nurses)
        m = len(self.patients)

        x = {}

        for i in range(n):
            for j in range(m):
                nurse = self.nurses[i]
                patient = self.patients[j]
                score = calculate_score(nurse,patient)

                if patient.required_shift in nurse.available_shifts:
                    x[i,j] = solver.IntVar(0,1,f'x[{i},{j}]')
                else:
                    x[i,j] = solver.IntVar(0,0, f'x[{i},{j}]')
        for j in range(m):
            solver.Add(solver.Sum(x[i,j] for i in range(n)) == 1)
        for i in range(n):
            solver.Add(solver.Sum(x[i,j] for j in range(m)) <= self.nurses[i].max_patients)
        num_patients = {}
        for i in range(n):
            num_patients[i] = solver.IntVar(0, self.nurses[i].max_patients, f'num_patients[{i}]')
            solver.Add(num_patients[i] == solver.Sum(x[i, j] for j in range(m)))
        stress_penalty_weight = 15
        stress_per_assignment = 2
        max_stress = 10
        objective = solver.Objective()

        for i in range(n):
            total_stress = self.nurses[i].current_stress + stress_per_assignment * num_patients[i]
            solver.Add(total_stress <= max_stress)

        for i in range(n):
            penalty = self.nurses[i].current_stress * num_patients[i]
            objective.SetCoefficient(num_patients[i], -self.nurses[i].current_stress)

        for i in range(n):
            for j in range(m):
                score = calculate_score(self.nurses[i],self.patients[j])
                objective.SetCoefficient(x[i,j],score)
            objective.SetCoefficient(num_patients[i],-stress_penalty_weight * self.nurses[i].current_stress)
        objective.SetMaximization()
        status = solver.Solve()
        assignments = []
        if status == pywraplp.Solver.OPTIMAL:
            print("Optimal assignment found:")
            for i in range(n):
                for j in range(m):
                    if x[i, j].solution_value() > 0.5:
                        nurse = self.nurses[i]
                        patient = self.patients[j]
                        score = calculate_score(nurse,patient)
                        assignments.append((nurse,patient,score))
            return assignments
        elif status == pywraplp.Solver.FEASIBLE:
            print("Feasable Assignment found: ")
            for i in range(n):
                for j in range(m):
                    if x[i, j].solution_value() > 0.5:
                        nurse = self.nurses[i]
                        patient = self.patients[j]
                        score = calculate_score(nurse,patient)
                        assignments.append((nurse,patient,score))
        else:
            print("No optimal solution found.")
            return(([],None,None))
