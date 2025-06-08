# main.py
from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
import joblib
import numpy as np
import os

# Get the directory where the current script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load model and encoders using safe absolute paths
model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
gender_encoder = joblib.load(os.path.join(MODEL_DIR, "gender_encoder.pkl"))
workout_encoder = joblib.load(os.path.join(MODEL_DIR, "workout_encoder.pkl"))

# Load accuracy



# Define request model
class UserProfile(BaseModel):
    Gender: str
    Age: int
    Height_cm: int
    Weight_kg: int
    Body_Fat_: float
    BMI: float
    BMR: int
    Max_BPM: int
    Avg_BPM: int
    Rest_BPM: int


# Create FastAPI instance
workout_router = APIRouter()


@workout_router.post("/predict_workout")
def predict_workout(data: UserProfile):
    # Encode gender
    gender_encoded = gender_encoder.transform([data.Gender])[0]

    # Prepare feature array
    features = np.array([[gender_encoded, data.Age, data.Height_cm, data.Weight_kg,
                          data.Body_Fat_, data.BMI, data.BMR,
                          data.Max_BPM, data.Avg_BPM, data.Rest_BPM]])

    # Predict
    prediction_encoded = model.predict(features)[0]
    prediction_label = workout_encoder.inverse_transform([prediction_encoded])[0]

    return {
        "predicted_workout_type": prediction_label,
    }
