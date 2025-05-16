from strategies.single_strategy import SinglePatientSolution
from strategies.automultipatient_strategy import AutoMultiPatientSolution
from tools.loaders import loadPatients, loadNurses
from tools.assignment_handler import submitTempAssignment, submitAssignment
from nurse_patient_classes import Nurse, NurseBuilder, PatientBuilder, Patient
"""
    Schedueling App!

    init vars:
        nurse_path: Path for json list of all nurses to be logged in
        patient_path: Path for json list of all patients to be logged in
        assignment_path: Path for output json of assignment list
    
    functions:
        run:
            passes strategy selection to select strategy
            receives a Solution Object that it then passes onto process
        select_strategy:
            allows users to select the strategy for assigning patients
            With a single patient it automatically passes it onto single solver
            returns a Solution Object
        process_strategy:
            passes solution object into its correct submition handler
        
        handle_single_patient:
            inputs:
                scored_nurses: list of nurses sorted by score match to patient
                patient: patient object
            Allows users to select which of the top return_limit (singlePatientSolution var) nurses
            Once selected passes nurse, patient and score to assign_nurse
        assign_nurse:
            called from handling of single patient
            inputs:
                nurse: nurse object
                patient: patient object
                score: Score between patient and Nurse
            logs nurse into the json specified by assignment path
            adds stress to nurse and removes shift from nurses available shifts
        handle_automulti_patients
            inputs:
                results:
                    tuple containing a list of (nurse,patient,score)
            logs all assignments into a temp file for user verification then logs to specified assignment path

"""
class SchedulerApp:
    def __init__(self, nurse_path, patient_path, assignment_path):
        self.nurse_list = loadNurses(nurse_path)
        self.patients = loadPatients(patient_path)
        self.assignment_path = assignment_path

    def run(self):
        while True:
            strategy = self.select_strategy(self.patients)
            if strategy is None:
                print("Patient matching cancelled")
                return
            self.process_strategy(strategy, self.patients)

    def select_strategy(self, patients):
        if len(patients) == 1:
            return SinglePatientSolution(self.nurse_list, patients[0], return_limit=10)
        else:
            while True:
                multi_sol_type = input("To match patients manually enter 0, to match automatically enter 1: ")
                if multi_sol_type == "0":
                    print("not implemented")
                    return #ManualMultiPatientSolution(self.nurse_list,patients) NEED TO IMPLEMENT
                if multi_sol_type == "1":
                    return AutoMultiPatientSolution(self.nurse_list,patients)
                if multi_sol_type == "exit":
                    break
            return None

    def process_strategy(self, strategy, patients):
        results = strategy.solve()
        if isinstance(strategy, SinglePatientSolution):
            self.handle_single_patient(results, patients[0])
        elif isinstance(strategy,AutoMultiPatientSolution):
            self.handle_automulti_patients(results,patients)
        else:
            self.handle_multi_patient(results)

    def handle_single_patient(self, scored_nurses, patient):
        if not scored_nurses:
            print("No nurse matches found.")
            return

        print(f"\nReturned {len(scored_nurses)} nurses. Select one by ID:\n")
        for nurse, score in scored_nurses:
            print(f"Nurse ID: {nurse.id}, Name: {nurse.name}, Stress: {nurse.current_stress}, Score: {score:.2f}")

        while True:
            selected = input("> ").strip()
            if selected.lower() == "exit":
                break
            for nurse, score in scored_nurses:
                if nurse.id == selected:
                    self.assign_nurse(nurse, patient,score)
                    return
            print("Invalid ID. Try again.")

    def assign_nurse(self, nurse, patient,score):
        print(f"Assigned Nurse {nurse.name} to Patient {patient.id}")
        nurse.current_stress += 2
        nurse.assigned_shifts.append(patient.required_shift)
        if patient.required_shift in nurse.available_shifts:
            nurse.available_shifts.remove(patient.required_shift)

        submitAssignment(self.assignment_path, {
            "nurse_id": nurse.id,
            "nurse_name": nurse.name,
            "patient_id": patient.id,
            "time": patient.required_shift,
            "score": score,
            "stress_level": nurse.current_stress
        })

    def handle_automulti_patients(self,results):
        if not results:
            print("No nurse matches found")
        else:
            data = []
            for nurse,patient,score in results:
                nurse.available_shifts.remove(patient.required_shift)
                data.append({
                    "nurse_id": nurse.id,
                    "nurse_name": nurse.name,
                    "patient_id": patient.id,
                    "time": patient.required_shift,
                    "score": score,
                    "nurse_stress": nurse.current_stress
                })
            submitTempAssignment("verifyout.json",data)
            while True:
                print("Inspect Verifyout.json the enter 1 to approve results and 0 to reject")
                ans = input()
                if ans.strip() == "1":
                    submitAssignment(self.assignment_path, data)
                    break
                elif ans.strip() == "0":
                    return None
                
    def handle_multi_patient(self, result):
        # Placeholder for multi-patient logic later
        pass
