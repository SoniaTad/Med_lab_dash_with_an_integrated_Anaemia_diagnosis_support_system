# main.py
from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from typing import List
from sklearn.preprocessing import StandardScaler

# Load the trained model
model = joblib.load('KNN_model.pkl')


# Define the input data model
class InputData(BaseModel):
    data: List[List[float]]

# Create a FastAPI app
app = FastAPI()

# Define the prediction endpoint
@app.post("/predict")
async def predict(data: InputData):
    scaler = joblib.load('scaler.pkl')
    input_data_scaled = scaler.transform(data.data)
    predictions = model.predict(input_data_scaled)
    return {"predictions": predictions.tolist()}