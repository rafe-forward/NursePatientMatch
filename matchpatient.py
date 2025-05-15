from nurse_patient_classes import Nurse, NurseBuilder, PatientBuilder,Patient
import json
from scipy.optimize import linear_sum_assignment
import numpy as np
from ortools.linear_solver import pywraplp
from abc import ABC, abstractmethod
from solution_strategy import SingleScheduleSolver
import os
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assignments.json")
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from loaders import loadPatients, loadNurses
from assignment_handler import submitAssignment
from scheduler_app import SchedulerApp
from solution_strategy import SinglePatientSolution#, MultiPatientSolution

if __name__ == "__main__":
    app = SchedulerApp(
        nurse_loader=lambda: loadNurses(""),
        patient_loader=loadPatients,
        assign_logger=submitAssignment
    )
    app.run()
    # nurse_list = loadNurses("")
    # for nurse in nurse_list:
    #     print(nurse)
    # while True:
    #     print("input path to patient.json")
    #     path = input().strip()
    #     if path.lower() == "exit":
    #         break
    #     try:
    #         patients = loadPatients(path)

    #         if len(patients) == 1:
    #             patient = patients[0]

    #             # Use strategy pattern here
    #             strategy = SinglePatientSolution(nurse_list, patient, return_limit=10)
    #             scored_nurses = strategy.solve()

    #             if scored_nurses:
    #                 print(f"Returned {len(scored_nurses)} Nurses, select one to cover the shift, enter their ID or type exit\n")
    #                 for nurse, score in scored_nurses:
    #                     print(f"Nurse ID: {nurse.id}, Nurse Name: {nurse.name}, Nurse Stress Level: {nurse.current_stress}, Match Score: {score:.2f}")

    #                 while True:
    #                     selected_nurse = input().strip()
    #                     if selected_nurse.lower() == "exit":
    #                         break
    #                     for nurse, score in scored_nurses:
    #                         if nurse.id == selected_nurse:
    #                             print(f"Nurse {nurse.name} scheduled for assignment")
    #                             nurse.current_stress += 2
    #                             nurse.assigned_shifts.append(patient.required_shift)
    #                             if patient.required_shift in nurse.available_shifts:
    #                                 nurse.available_shifts.remove(patient.required_shift)
    #                             data = {
    #                                 "nurse_id": nurse.id,
    #                                 "nurse_name": nurse.name,
    #                                 "patient_id": patient.id,
    #                                 "time": patient.required_shift
    #                             }
    #                             submitAssignment("assignments.json", data)
    #                             break
    #                     else:
    #                         print("Nurse not found in the list. Try again.")
    #             else:
    #                 print("No matches")

    #         else:
    #             # TODO: Add MultiPatientSolution integration here later
    #             print("🧠 Multi-patient input detected. Optimization-based strategy coming soon.")
    #             # Example:
    #             # strategy = MultiPatientSolution(nurse_list, patients)
    #             # assignments, score, runtime = strategy.solve()
    #             # for nurse, patient, match_score in assignments:
    #             #     ...
    #     except FileNotFoundError:
    #         print("File not found, please try again\n")
    #     except Exception as e:
    #         print(f"Unexpected error: {type(e).__name__} - {e}\n")

        