from cli.assignment_display import display_assignments
class SchedulerApp:
    def __init__(self, nurses, patients):
        self.nurses = nurses
        self.patients = patients

    def run_strategy(self, strategy):
        results = strategy.solve()

        
        if isinstance(results, tuple) and len(results) == 2:
            return results

        return results, [] 
