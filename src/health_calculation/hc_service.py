def calculate_protein_intake(
        weight_kg: float,
        goal: str = "maintain",
        activity_level: str = "moderate",
        age: int = 25,
        meals_per_day: int = 3
) -> dict:
    goal = goal.lower()
    activity_level = activity_level.lower()

    goal_multipliers = {
        "maintain": 1.2,
        "lose": 1.5,
        "gain": 2.0
    }

    activity_multipliers = {
        "sedentary": 1.0,
        "moderate": 1.1,
        "active": 1.2
    }

    if goal not in goal_multipliers:
        raise ValueError("Invalid goal. Use 'maintain', 'lose', or 'gain'.")
    if activity_level not in activity_multipliers:
        raise ValueError("Invalid activity level. Use 'sedentary', 'moderate', or 'active'.")
    if meals_per_day <= 0:
        raise ValueError("Meals per day must be at least 1.")

    multiplier = goal_multipliers[goal] * activity_multipliers[activity_level]
    if age >= 60:
        multiplier += 0.2

    total_protein = round(weight_kg * multiplier, 2)
    protein_per_meal = round(total_protein / meals_per_day, 2)

    return {
        "total_protein_grams": total_protein,
        "meals_per_day": meals_per_day,
        "protein_per_meal_grams": protein_per_meal
    }


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    gender = gender.lower()
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Must be 'male' or 'female'.")

    return round(bmr, 2)


def calculate_heart_rate(age: int) -> dict:
    if age <= 0 or age >= 120:
        raise ValueError("Age must be between 1 and 120.")

    max_bpm = 220 - age
    avg_bpm_lower = round(max_bpm * 0.50)
    avg_bpm_upper = round(max_bpm * 0.85)

    return {
        "max_bpm": max_bpm,
        "average_bpm_range": f"{avg_bpm_lower} - {avg_bpm_upper} bpm",
        "average_bpm_lower": avg_bpm_lower,
        "average_bpm_upper": avg_bpm_upper
    }


def calculate_tdee(bmr: float, activity_level: str) -> float:
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    level = activity_level.lower()
    if level not in activity_multipliers:
        raise ValueError("Invalid activity level.")
    return round(bmr * activity_multipliers[level], 2)
