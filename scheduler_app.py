from solution_strategy import SinglePatientSolution#, MultiPatientSolution
class SchedulerApp:
    def __init__(self, nurse_loader, patient_loader, assign_logger):
        self.nurse_list = nurse_loader()
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
                self.process_strategy(strategy, patients)
            except FileNotFoundError:
                print("File not found. Try again.")
            except Exception as e:
                print(f"Unexpected error: {type(e).__name__} - {e}")

    def select_strategy(self, patients):
        if len(patients) == 1:
            return SinglePatientSolution(self.nurse_list, patients[0], return_limit=10)
        else:
            return #MultiPatientSolution(self.nurse_list, patients)

    def process_strategy(self, strategy, patients):
        results = strategy.solve()
        if isinstance(strategy, SinglePatientSolution):
            self.handle_single_patient(results, patients[0])
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
                    self.assign_nurse(nurse, patient)
                    return
            print("Invalid ID. Try again.")

    def assign_nurse(self, nurse, patient):
        print(f"Assigned Nurse {nurse.name} to Patient {patient.id}")
        nurse.current_stress += 2
        nurse.assigned_shifts.append(patient.required_shift)
        if patient.required_shift in nurse.available_shifts:
            nurse.available_shifts.remove(patient.required_shift)

        self.log_assignment("assignments.json", {
            "nurse_id": nurse.id,
            "nurse_name": nurse.name,
            "patient_id": patient.id,
            "time": patient.required_shift
        })

    def handle_multi_patient(self, result):
        # Placeholder for multi-patient logic later
        pass
