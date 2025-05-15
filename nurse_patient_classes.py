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


###Patient Builder
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
class Nurse_Patient_Val:
    def __init__(self, nurse, patient):
        self.nurse = nurse
        self.patient = patient
        self.score = self.calculate_score()

    def calculate_score(self):
        score = 50

        stress_score = (self.nurse.current_stress ** 2) / 2
        score -= stress_score

        if self.nurse.id in self.patient.preferred_nurse_ids:
            score += 20

        if self.patient.condition in self.nurse.skills:
            score += 20

        if self.patient.required_shift in self.nurse.available_shifts:
            score += 20
        else:
            score -= 40

        return max(score, 0.1)

    def __str__(self):
        return f"Nurse: {self.nurse.name}, Patient ID: {self.patient.id}, Score: {self.score}"

        