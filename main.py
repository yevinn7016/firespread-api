from fastapi import FastAPI, Request
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import os
import json

# 🔐 환경 변수에서 Firebase 키 불러오기
if not firebase_admin._apps:
    firebase_json = os.environ.get("FIREBASE_KEY")
    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    initialize_app(cred)

db = firestore.client()
app = FastAPI()
input_queue = []

@app.post("/input")
async def receive_input(request: Request):
    data = await request.json()
    input_queue.append(data)
    return {"status": "input received"}

@app.get("/check_input")
def check_input():
    if input_queue:
        return input_queue[-1]  # 가장 최근 입력 반환
    else:
        return {}

@app.post("/result")
async def receive_result(request: Request):
    data = await request.json()
    lat = str(data.get("center_lat"))
    lon = str(data.get("center_lon"))
    doc_id = f"{lat}_{lon}"
    db.collection("fire_results").document(doc_id).set(data)
    return {"status": "result saved"}
