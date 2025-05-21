from tools.loaders import loadNurses, loadPatients
from tools.assignment_handler import submitAssignment
from cli.strategy_factory import StrategyFactory
from cli.assignment_display import display_assignments, confirm_submission
from strategies.automultipatient_strategy import AutoMultiPatientSolution
from strategies.manualmultipatient_strategy import ManualMultiPatientSolution
from core.scheduler_app import SchedulerApp

def interactive_selection(strategy):
    selected = []
    for patient, scored_nurses in strategy.solve():
        print(f"\nChoose nurse for Patient {patient.id} ({patient.condition} @ {patient.required_shift}):")
        for i, (nurse, score) in enumerate(scored_nurses):
            print(f"[{i}] {nurse.name} (Score: {score:.2f}) (Stress: {nurse.current_stress})")
        choice = input("Enter number (or press Enter to skip): ").strip()
        if choice.isdigit():
            i = int(choice)
            if 0 <= i < len(scored_nurses):
                nurse, score = scored_nurses[i]
                nurse.current_stress += 2
                selected.append((nurse, patient, score))
    return selected

def main():
    nurse_path = "data/nurses_hard.json"
    patient_path = "data/patients_hard.json"
    assignment_path = "assignments.json"

    nurses = loadNurses(nurse_path)
    patients = loadPatients(patient_path)
    if not nurses or not patients:
        print("Missing nurse or patient data.")
        return

    scheduler = SchedulerApp(nurses, patients)

    while True:
        strategy = StrategyFactory.select_strategy(patients, nurses)
        if not strategy:
            print("Exiting scheduler.")
            break

        result = scheduler.run_strategy(strategy)


        if isinstance(result, tuple) and len(result) == 2:
            assignments, unmatched = result
        else:
            assignments = result
            unmatched = []

        # If no assignments and using manual strategy, do interactive selection
        if not assignments and isinstance(strategy, ManualMultiPatientSolution):
            assignments = interactive_selection(strategy)

        display_assignments(assignments)

        # Retry unmatched patients (if any)
        if unmatched:
            print(f"\n{len(unmatched)} patients were not matched.")
            retry = input("Try to match the rest manually? (y/n): ").strip().lower()
            if retry == "y":
                manual_strategy = ManualMultiPatientSolution(nurses, unmatched)
                assignments += interactive_selection(manual_strategy)

        # Save assignments
        if confirm_submission():
            submitAssignment(assignment_path, assignments)
            print("Assignments submitted.")
            break
        else:
            print("Assignment canceled.")
            break

if __name__ == "__main__":
    main()
