from fastapi import FastAPI, Request
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

# 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("firespreadapp-firebase-adminsdk-fbsvc-5acff07d40.json")  # 파일명에 맞게
    initialize_app(cred)
db = firestore.client()

app = FastAPI()
input_queue = []

@app.post("/input")
async def receive_input(request: Request):
    data = await request.json()
    input_queue.append(data)
    return {"status": "input received"}

# ✅ 수정된 check_input: pop() → peek (보기만)
@app.get("/check_input")
def check_input():
    if input_queue:
        return input_queue[-1]  # 마지막 입력 반환 (삭제하지 않음)
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
