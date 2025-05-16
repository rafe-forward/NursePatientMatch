class Nurse:
    def __init__(self, id, name, skills, available_shifts,max_patients,current_stress):
        self.id = id
        self.name = name
        self.skills = skills
        self.available_shifts = available_shifts
        self.max_patients = max_patients
        self.current_stress = current_stress
        self.assigned_shifts = []
    def __str__(self):
        return f"Name: {self.name}"
    
#Use nurse builder for future scalability. Plans for additional attributes which may or may not be implemented
#for every instance
class NurseBuilder:
    def __init__(self):
        self.id = None
        self.name = None
        self.skills = None
        self.available_shifts = None
        self.max_patients = None
        self.current_stress = None
    def set_id(self,id):
        self.id = id
        return self
    def set_name(self,name):
        self.name = name
        return self
    def set_skills(self,skills):
        self.skills = skills
        return self
    def set_available_shifts(self,available_shifts):
        self.available_shifts = available_shifts
        return self
    def set_max_patients(self,max_patients):
        self.max_patients = max_patients
        return self
    def set_current_stress(self, current_stress):
        self.current_stress = current_stress
        return self
    def build(self):
        return Nurse(
            self.id,
            self.name,
            self.skills,
            self.available_shifts,
            self.max_patients,
            self.current_stress
        )
    
###Patient class
class Patient:
    def __init__(self, id, condition, preferred_nurse_ids, required_shift, priority):
        self.id = id
        self.condition = condition
        self.preferred_nurse_ids = preferred_nurse_ids
        self.required_shift = required_shift
        self.priority = priority

    def __str__(self):
        return f"Patient ID: {self.id}, Condition: {self.condition}, Priority: {self.priority}"


"Patient Builder, similar to nurse builder, plans of future attribute expansion so keep as builder"
class PatientBuilder:
    def __init__(self):
        self.id = None
        self.condition = None
        self.preferred_nurse_ids = None
        self.required_shift = None
        self.priority = None

    def set_id(self, id):
        self.id = id
        return self

    def set_condition(self, condition):
        self.condition = condition
        return self

    def set_preferred_nurse_ids(self, preferred_nurse_ids):
        self.preferred_nurse_ids = preferred_nurse_ids
        return self

    def set_required_shift(self, required_shift):
        self.required_shift = required_shift
        return self

    def set_priority(self, priority):
        self.priority = priority
        return self

    def build(self):
        return Patient(
            self.id,
            self.condition,
            self.preferred_nurse_ids,
            self.required_shift,
            self.priority
        )
"""Currently not in use, could be very helpful for future assignment processing"""
class Assignment:
    def __init__(self, nurse_id, nurse_name,patient_id,time,score):
        self.nurse_id = nurse_id
        self.nurse_name = nurse_name
        self.patient_id = patient_id
        self.time = time
        self.score = score
    def to_dict(self):
        data = {
            "nurse_id": f"{self.nurse_id}",
            "nurse_name": f"{self.nurse_name}",
            "patient_id": f"{self.patient_id}",
            "time": f"{self.time}",
            "score": f"{self.score}"
        }
        return data
        