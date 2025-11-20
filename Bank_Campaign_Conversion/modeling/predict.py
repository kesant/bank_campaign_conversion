import pickle
from typing import Literal
from pydantic import BaseModel, Field
from Bank_Campaign_Conversion.utils.paths import data_raw_dir,models_dir

from fastapi import FastAPI
import uvicorn

# define the data model
class Customer(BaseModel):
    poutcome: Literal["unknown", "failure", "other", "success"]
    month: Literal["may", "jul", "aug", "jun", "nov", "apr", "feb", "jan", "oct", "sep", "mar", "dec"]
    contact: Literal["cellular", "unknown", "telephone"]
    duration: int = Field(..., ge=0)
    pdays: int = Field(..., ge=-1)
    balance: float = Field(..., ge=-8019.0)
    previous: int = Field(..., ge=0)
    age: int = Field(..., ge=18)

class PredictResponse(BaseModel):
    convertion_probability: float
    converted: bool

app = FastAPI(title="investment offer convertion prediction API")

# Load the model
with open(models_dir("logistic_regresion.pkl"), 'rb') as f_in:
    pipeline = pickle.load(f_in)

# 
def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


@app.post("/predict")
def predict(customer: Customer) -> PredictResponse:
    # 
    customer_dict = customer.dict()
    
    # 
    prob = predict_single(customer_dict)
    
    # Devuelve la respuesta en el formato requerido
    return PredictResponse(
        convertion_probability=prob,
        converted=prob >= 0.35
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)




