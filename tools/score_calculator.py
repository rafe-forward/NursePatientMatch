"""
Arbitrary score calculation factoring in condition preference stress and available shifts
"""


def calculate_score(nurse, patient):
    score = 50

    stress_score = (nurse.current_stress**2) / 2
    score -= stress_score

    if nurse.id in patient.preferred_nurse_ids:
        score += 20

    if patient.condition in nurse.skills:
        score += 20

    if patient.required_shift in nurse.available_shifts:
        score += 20
    else:
        score -= 40

    return max(score, 0.1)
