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
        nurse_path="nurses.json",
        patient_loader=loadPatients,
        assign_logger=submitAssignment
    )
    app.run()
