# main.py
from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
import numpy as np
import joblib
import os

# Define base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_model.pkl")

# Load the churn model
model = joblib.load(MODEL_PATH)


class ChurnInput(BaseModel):
    gender: int
    Near_Loca: int
    Partner: int
    Promo_frik: int
    Phone: int
    Contract_r: int
    Group_visi: int
    Age: int
    Month_to: int
    Lifetime: int
    Avg_class_frequer: float
    Avg_class_frequer_1: float


churn_router = APIRouter()



@churn_router.post("/predict_churn")
def predict_churn(data: ChurnInput):
    features = np.array([[data.gender, data.Near_Loca, data.Partner, data.Promo_frik,
                          data.Phone, data.Contract_r, data.Group_visi, data.Age,
                          data.Month_to, data.Lifetime,
                          data.Avg_class_frequer, data.Avg_class_frequer_1]])

    prediction = model.predict(features)[0]
    return {
        "churn_prediction": int(prediction)
    }
