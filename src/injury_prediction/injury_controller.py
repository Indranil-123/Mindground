from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import joblib
import os

in_router = APIRouter()

model_path = os.path.join(os.path.dirname(__file__), "ml_model", "injury_classifier_model.pkl")
model = joblib.load(model_path)


class SentenceInput(BaseModel):
    sentence: str


@in_router.post("/predict-injury")
def predict_injury_api(input: SentenceInput):
    prediction = model.predict([input.sentence])[0]
    return {"predicted_injury": prediction}