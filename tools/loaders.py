import json
from nurse_patient_classes import PatientBuilder, NurseBuilder
def loadPatients(path):
    patient_list = []
    with open(path, 'r') as f:
        data = json.load(f)
        patient_builder = PatientBuilder()
        for pat in data:
            patient = patient_builder.set_id(str(pat["id"]))\
        .set_condition(pat["condition"])\
        .set_preferred_nurse_ids([str(nid) for nid in pat["preferred_nurse_ids"]])\
        .set_required_shift(pat["required_shift"])\
        .set_priority(pat["priority"])\
        .build()
            patient_list.append(patient)
        return patient_list

def loadNurses(path):
    nurse_list = []
    with open("nurses.json", 'r') as f:
        data = json.load(f)
        for nur in data:
            nurse_builder = NurseBuilder()
            nurse = nurse_builder.set_id(str(nur["id"])).set_name(nur["name"]).set_skills(nur["skills"]).set_available_shifts(nur["available_shifts"]).set_max_patients(nur["max_patients"]).set_current_stress(nur["current_stress"]).build()
            print(f"appending nurse {nurse.id}")
            nurse_list.append(nurse)
    print(nurse_list)
    return nurse_list