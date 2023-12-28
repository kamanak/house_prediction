import pickle
from fastapi import FastAPI,HTTPException
import numpy as np
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    MedInc: float
    HouseAge:float
    AveRooms:float
    AveBedrms:float
    Population:float
    AveOccup:float
    Latitude:float
    Longitude:float
    
class Outputdata(BaseModel):
    prediction: float

model = pickle.load(open('regmodel.pkl','rb'))
scaler = pickle.load(open('scaling.pkl','rb'))

def make_prediction(data: InputData):
    try:
        data_dict = data.dict()
        print(f"Input data: {data_dict}")

        for key in InputData.__annotations__.keys():
            data_dict.setdefault(key, 0.0)

        input_array = np.array([data_dict['MedInc'], data_dict['HouseAge'], data_dict['AveRooms'],
                                data_dict['AveBedrms'], data_dict['Population'], data_dict['AveOccup'],
                                data_dict['Latitude'], data_dict['Longitude']]).reshape(1, -1)

        new_data = scaler.transform(input_array)
        output = model.predict(new_data)
        prediction_value = float(output.item())
        return prediction_value 
    except Exception as e:
        print(f"Error in make_prediction: {e}")
        print(f"Exception details: {str(e)}")
        raise e


@app.post('/predict', response_model=Outputdata)
async def predict(data: InputData):
    try:
        print(f"Received request with data: {data.dict()}")
        result = make_prediction(data)
        return Outputdata(prediction=result)
    except Exception as e:
        print(f"Error in predict route: {e}")
        raise HTTPException(status_code=400, detail=str(e))


