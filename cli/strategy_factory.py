from strategies.single_strategy import SinglePatientSolution
from strategies.automultipatient_strategy import AutoMultiPatientSolution
from strategies.manualmultipatient_strategy import ManualMultiPatientSolution

MODELTYPE = "lp"

class StrategyFactory:
    @staticmethod
    def select_strategy(patients, nurses):
        """
        Chooses the appropriate matching strategy based on number of patients and user input.
        Returns an object with a `.solve()` method conforming to MatchingStrategy.
        """

        while True:
            print("\nChoose a matching mode:")
            print("  [1] Auto-match (solver-based)")
            print("  [0] Manual-match (interactive)")
            print("  [exit] Cancel")

            choice = input("Your choice: ").strip().lower()
            if choice == "1":
                return AutoMultiPatientSolution(nurses, patients, MODELTYPE)
            elif choice == "0":
                return ManualMultiPatientSolution(nurses, patients, return_limit=10)
            elif choice == "exit":
                return None
            else:
                print("Invalid input. Please enter 1, 0, or 'exit'.")
