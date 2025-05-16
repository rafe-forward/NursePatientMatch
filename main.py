import sys
import os
from scheduler_app import SchedulerApp
from strategies.single_strategy import SinglePatientSolution
from strategies.automultipatient_strategy import AutoMultiPatientSolution
from tools.loaders import loadPatients
from tools.assignment_handler import submitAssignment
def select_strategy(nurses, patients):
    if len(patients) == 1:
        return SinglePatientSolution(nurses, patients[0], return_limit=10)
    else:
        while True:
            choice = input("Multi-patient match: 0 for manual, 1 for auto, 'exit' to cancel: ").strip()
            if choice == "1":
                return AutoMultiPatientSolution(nurses, patients)
            elif choice == "0":
                print("ManualMultiPatientSolution not implemented.")
            elif choice.lower() == "exit":
                return None
            else:
                print("Invalid input. Try 0, 1, or 'exit'.")

def main():
    app = SchedulerApp(
        nurse_path="./data/nurses.json",
        patient_loader=loadPatients,
        assign_logger=submitAssignment
    )
    app.run()

if __name__ == "__main__":
    main()