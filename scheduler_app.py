from solution_strategy import SinglePatientSolution, AutoMultiPatientSolution
from loaders import loadPatients, loadNurses
from assignment_handler import submitTempAssignment
from nurse_patient_classes import Nurse, NurseBuilder, PatientBuilder,Patient, Assignment
class SchedulerApp:
    def __init__(self, nurse_path, patient_loader, assign_logger):
        self.nurse_list = loadNurses(nurse_path)
        self.patient_loader = patient_loader
        self.log_assignment = assign_logger

    def run(self):
        while True:
            path = input("Input path to patient.json (or 'exit'): ").strip()
            if path.lower() == "exit":
                break
            try:
                patients = self.patient_loader(path)
                strategy = self.select_strategy(patients)
                if strategy is None:
                    print("Patient matching cancelled")
                    return
                self.process_strategy(strategy, patients)
            except FileNotFoundError:
                print("File not found. Try again.")
            except Exception as e:
                print(f"Unexpected error: {type(e).__name__} - {e}")

    def select_strategy(self, patients):
        if len(patients) == 1:
            return SinglePatientSolution(self.nurse_list, patients[0], return_limit=10)
        else:
            while True:
                multi_sol_type = input("To match patients manually enter 0, to match automatically enter 1")
                if multi_sol_type == "0":
                    return ManualMultiPatientSolution(self.nurse_list,patients)
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

        self.log_assignment("assignments.json", {
            "nurse_id": nurse.id,
            "nurse_name": nurse.name,
            "patient_id": patient.id,
            "time": patient.required_shift,
            "score": score,
            "stress_level": nurse.current_stress
        })

    def handle_automulti_patients(self,results,patients):
        if not results:
            print("No nurse matches found")
        else:
            data = []
            for assigned_nurse,assigned_patient,score in results:
                data.append({
                    "nurse_id": assigned_nurse.id,
                    "nurse_name": assigned_nurse.name,
                    "patient_id": assigned_patient.id,
                    "time": assigned_patient.required_shift,
                    "score": score,
                    "nurse_stress": assigned_nurse.current_stress
                })
            submitTempAssignment("verifyout.json",data)
            while True:
                print("Inspect Verifyout.json the enter 1 to approve results and 0 to reject")
                ans = input()
                if ans.strip() == "1":
                    self.log_assignment("assignments.json", data)
                    break
                elif ans.strip() == "0":
                    return None
                
    def handle_multi_patient(self, result):
        # Placeholder for multi-patient logic later
        pass
