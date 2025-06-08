from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.chat_module import chat_controller
from src.health_calculation import hc_controller
from src.injury_prediction import injury_controller
from src.workout_type import workout_prediction_controller
from src.churn_prediction import churn_prediction_controller

app = FastAPI()

app.include_router(chat_controller.router)
app.include_router(hc_controller.calc_router)
app.include_router(injury_controller.in_router)
app.include_router(workout_prediction_controller.workout_router)
app.include_router(churn_prediction_controller.churn_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}
