from nurse_patient_classes import Nurse, NurseBuilder, PatientBuilder,Patient
import json
from hungarian_algorithm import algorithm
from scipy.optimize import linear_sum_assignment
import numpy as np
builder = NurseBuilder()

patient_list = []
with open('patients.json', 'r') as f:
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
with open('nurses.json', 'r') as f:
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

for i, j in zip(row_ind, col_ind):
    print(f"Nurse {nurse_ids[i]} → Patient {patient_ids[j]}, Score: {-score_matrix[i][j]}")
