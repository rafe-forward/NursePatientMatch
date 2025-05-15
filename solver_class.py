import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from loaders import loadPatients, loadNurses
from assignment_handler import submitAssignment

class Solver:
    def __init__(self,count,manual):
        self.count = 