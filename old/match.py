from nurse_patient_classes import Nurse, NurseBuilder, PatientBuilder,Patient
import json
from scipy.optimize import linear_sum_assignment
import numpy as np
from ortools.linear_solver import pywraplp
builder = NurseBuilder()

patient_list = []
with open('patients_hard.json', 'r') as f:
    data = json.load(f)
    patient_builder = PatientBuilder()
    ctr = 0
    for pat in data:
        patient = patient_builder.set_id(str(pat["id"]))\
    .set_condition(pat["condition"])\
    .set_preferred_nurse_ids([str(nid) for nid in pat["preferred_nurse_ids"]])\
    .set_required_shift(pat["required_shift"])\
    .set_priority(pat["priority"])\
    .build()
        patient_list.append(patient)


nurse_list = []
with open('nurses_hard.json', 'r') as f:
    data = json.load(f)
    nurse_builder = NurseBuilder()
    ctr = 0
    for nur in data:
        nurse = nurse_builder.set_id(str(nur["id"]))\
    .set_name(nur["name"])\
    .set_skills(nur["skills"])\
    .set_available_shifts(nur["available_shifts"])\
    .set_max_patients(nur["max_patients"])\
    .set_current_stress(nur["current_stress"])\
    .build()

        nurse_list.append(nurse)
    def calculate_score(nurse,patient):
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

    def __str__(self):
        return f"Nurse: {self.nurse.name}, Patient ID: {self.patient.id}, Score: {self.score}"
G = {}
ctr =0

nurse_ids = [n.id for n in nurse_list]
patient_ids = [p.id for p in patient_list]
score_matrix = np.zeros((len(nurse_ids), len(patient_ids)))

for i, nurse in enumerate(nurse_list):
    for j, patient in enumerate(patient_list):
        score_matrix[i][j] = -calculate_score(nurse, patient)

row_ind, col_ind = linear_sum_assignment(score_matrix)
final_Score = 0
for i, j in zip(row_ind, col_ind):
    print(f"Nurse {nurse_ids[i]} → Patient {patient_ids[j]}, Score: {-score_matrix[i][j]}")
    final_Score += score_matrix[i][j]

print(abs(final_Score))
solver = pywraplp.Solver.CreateSolver("SCIP")
if not solver: 
    raise Exception("SCIP solver is not available")
n = len(nurse_list)
m = len(patient_list)

x = {}

for i in range(n):
    for j in range(m):
        nurse = nurse_list[i]
        patient = patient_list[j]
        score = calculate_score(nurse,patient)

        if patient.required_shift in nurse.available_shifts:
            x[i,j] = solver.IntVar(0,1,f'x[{i},{j}]')
        else:
            x[i,j] = solver.IntVar(0,0, f'x[{i},{j}]')
for j in range(m):
    solver.Add(solver.Sum(x[i,j] for i in range(n)) == 1)
for i in range(n):
    solver.Add(solver.Sum(x[i,j] for j in range(m)) <= nurse_list[i].max_patients)
num_patients = {}
for i in range(n):
    num_patients[i] = solver.IntVar(0, nurse_list[i].max_patients, f'num_patients[{i}]')
    solver.Add(num_patients[i] == solver.Sum(x[i, j] for j in range(m)))
stress_penalty_weight = 5
stress_per_assignment = 2
max_stress = 10
objective = solver.Objective()

for i in range(n):
    total_stress = nurse_list[i].current_stress + stress_per_assignment * num_patients[i]
    solver.Add(total_stress <= max_stress)

for i in range(n):
    penalty = nurse_list[i].current_stress * num_patients[i]
    objective.SetCoefficient(num_patients[i], -nurse_list[i].current_stress)

for i in range(n):
    for j in range(m):
        score = calculate_score(nurse_list[i],patient_list[j])
        objective.SetCoefficient(x[i,j],score)
    objective.SetCoefficient(num_patients[i],-stress_penalty_weight * nurse_list[i].current_stress)
objective.SetMaximization()
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Optimal assignment found:")
    for i in range(n):
        for j in range(m):
            if x[i, j].solution_value() > 0.5:
                nurse = nurse_list[i]
                patient = patient_list[j]
                print(f"Nurse {nurse.id} → Patient {patient.id}, Score: {calculate_score(nurse, patient)} - Nurse Stress: {nurse.current_stress}")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print("Total score:", objective.Value())
else:
    print("No optimal solution found.")
if status == pywraplp.Solver.FEASIBLE:
    print("Feasable Assignment found: ")
    for i in range(n):
        for j in range(m):
            if x[i, j].solution_value() > 0.5:
                nurse = nurse_list[i]
                patient = patient_list[j]
                print(f"Nurse {nurse.id} → Patient {patient.id}, Score: {calculate_score(nurse, patient)} - Nurse Stress: {nurse.current_stress}")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print("Total score feasible :", objective.Value())
