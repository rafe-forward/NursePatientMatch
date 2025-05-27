from tools.loaders import loadNurses, loadPatients
from core.scheduler_app import SchedulerApp
from strategies.automultipatient_strategy import AutoMultiPatientSolution
from tools.assignment_handler import submitAssignment, assignments_to_dict
def match_nurses_patients(nurses,patients):
    if not nurses:
        nurses = loadNurses("data/nurses.json")
    if not patients:
        patients = loadPatients("data/patients.json")
    scheduler = SchedulerApp(nurses,patients)
    strategy = AutoMultiPatientSolution(nurses,patients, "lp")
    result = scheduler.run_strategy(strategy)
    if isinstance(result, tuple) and len(result) == 2:
        assignments, unmatched = result
    else:
        assignments = result
        unmatched = []
    if unmatched:
        print("There are some unmatched")
    assignment_dict = assignments_to_dict(assignments)

    return assignment_dict

    

        