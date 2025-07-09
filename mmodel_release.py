# server.py
from fastapi import FastAPI
from pydantic import BaseModel
import matlab.engine

app = FastAPI()
eng = matlab.engine.start_matlab()  # MATLAB 엔진 시작
eng.cd(r"C:\mat", nargout=0)  # m파일 경로

class InputData(BaseModel):
    value: float

@app.post("/predict")
def predict(data: InputData):
    result = eng.fire_predict(float(data.value))
    return {"input": data.value, "result": result}
