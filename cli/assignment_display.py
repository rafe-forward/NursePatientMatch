def display_assignments(assignments):
    if not assignments:
        print("No matches found.")
        return

    print(f"\n{len(assignments)} patient(s) matched:\n")
    for nurse, patient, score in assignments:
        print(f"Nurse {nurse.name} → Patient {patient.id} @ {patient.required_shift} (Score: {score:.2f})")

def confirm_submission():
    while True:
        ans = input("Submit these assignments? (1 = yes, 0 = no): ").strip()
        if ans == "1":
            return True
        elif ans == "0":
            return False
        else:
            print("Invalid input.")

