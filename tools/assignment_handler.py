import os
import json

"""
submitAssignment:
    function passed in to scheduler app in main then later used in both singlesolver and automultisolver
    Use to place assigned data from x into assignments.json
submitTempAssignment:
    Used to place data from automultisolver in verifyout before it is confirmed by user
"""
def submitAssignment(file_path, data):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            try:
                assignment_list = json.load(json_file)
                if not isinstance(assignment_list, list):
                    assignment_list = []
            except json.JSONDecodeError:
                assignment_list = []
    else:
        assignment_list = []

    assignment_list = data if isinstance(data, list) else [data]

    with open(file_path, 'w') as json_file:
        out = [
            {
                "nurse_id": nurse.id,
                "nurse_name": nurse.name,
                "patient_id": patient.id,
                "condition": patient.condition,
                "required_shift": patient.required_shift,
                "score": score
            }
            for (nurse, patient, score) in assignment_list
        ]

        json.dump(out, json_file, indent=4)

    print(f"Appended {len(data) if isinstance(data, list) else 1} assignment(s) to '{file_path}'")

def submitTempAssignment(file_path,data):
    with open(file_path, "w") as json_file:
        json.dump(data,json_file,indent=4)
    
def assignments_to_dict(data):
    assignment_list = data if isinstance(data, list) else [data]
    out = [
    {
        "nurse_id": nurse.id,
        "nurse_name": nurse.name,
        "patient_id": patient.id,
        "condition": patient.condition,
        "required_shift": patient.required_shift,
        "score": score
    }
    for (nurse, patient, score) in assignment_list
    ]
    return out