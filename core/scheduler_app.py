from cli.assignment_display import display_assignments, display_candidate_options
class SchedulerApp:
    def __init__(self, nurses, patients):
        self.nurses = nurses
        self.patients = patients

    def run_strategy(self, strategy):
        results = strategy.solve()

        
        if isinstance(results, tuple) and len(results) == 2:
            return results

        if isinstance(results, list) and all(isinstance(r, tuple) and isinstance(r[1], list) for r in results):
            display_candidate_options(results)

            return [], []

        return results, [] 
