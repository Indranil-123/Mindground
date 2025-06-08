from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from src.health_calculation.hc_service import calculate_protein_intake, calculate_bmr, calculate_heart_rate, calculate_tdee

calc_router = APIRouter()


class ProteinRequest(BaseModel):
    weight_kg: float
    goal: str = "maintain"
    activity_level: str = "moderate"
    age: int = 25
    meals_per_day: int = 3


class FitnessRequest(BaseModel):
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    goal: str = "maintain"  # lose, gain, maintain
    activity_level: str = "moderate"  # sedentary, light, moderate, active, very_active
    meals_per_day: int = 3


class BPMRequest(BaseModel):
    age: int


class BMRRequest(BaseModel):
    weight_kg: float
    height_cm: float
    age: int
    gender: str


@calc_router.post("/protein_intake")
def Calc_Protein(data: ProteinRequest):
    try:
        result = calculate_protein_intake(
            weight_kg=data.weight_kg,
            goal=data.goal,
            activity_level=data.activity_level,
            age=data.age,
            meals_per_day=data.meals_per_day
        )
        return result
    except ValueError as e:
        return {"error": str(e)}


@calc_router.post("/calculate-bmr")
def get_bmr(data: BMRRequest):
    try:
        bmr = calculate_bmr(
            weight_kg=data.weight_kg,
            height_cm=data.height_cm,
            age=data.age,
            gender=data.gender
        )
        return {"bmr_kcal_per_day": bmr}
    except ValueError as e:
        return {"error": str(e)}


@calc_router.post("/calculate-bpm")
def get_bpm(data: BPMRequest):
    try:
        result = calculate_heart_rate(age=data.age)
        return result
    except ValueError as e:
        return {"error": str(e)}


@calc_router.post("/fitness-profile")
def generate_fitness_profile(data: FitnessRequest):
    try:
        bmr = calculate_bmr(data.weight_kg, data.height_cm, data.age, data.gender)
        tdee = calculate_tdee(bmr, data.activity_level)
        protein_info = calculate_protein_intake(
            weight_kg=data.weight_kg,
            goal=data.goal,
            activity_level=data.activity_level,
            age=data.age,
            meals_per_day=data.meals_per_day
        )
        heart_rate = calculate_heart_rate(data.age)

        return {
            "bmr_kcal_per_day": bmr,
            "tdee_kcal_per_day": tdee,
            "protein_intake": protein_info,
            "heart_rate_info": heart_rate
        }

    except ValueError as e:
        return {"error": str(e)}
