from fastapi import FastAPI, Request
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import os
import json

# 🔐 Firebase 초기화
if not firebase_admin._apps:
    firebase_json = os.environ.get("FIREBASE_KEY")
    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    initialize_app(cred)

db = firestore.client()
app = FastAPI()

# 🔁 기존 input 유지 (선택)
input_queue = []

@app.post("/input")
async def receive_input(request: Request):
    data = await request.json()
    input_queue.append(data)
    return {"status": "input received"}

@app.get("/check_input")
def check_input():
    if input_queue:
        return input_queue[-1]
    else:
        return {}

# ✅ 예빈님 구조 반영: 전체 결과 저장
@app.post("/upload_result")
async def upload_result(request: Request):
    data = await request.json()

    # 🔸 문제 ID: "1", "2", "3" 등
    problem_id = str(data.get("problem_id", "unknown"))
    grid_results = data.get("grid_results", [])
    global_top3 = data.get("global_top3", [])

    # 🔁 grid_id를 기준으로 결과 묶기
    grids_map = {
        f"grid_{g['grid_id']}": {
            "grid_id": g["grid_id"],
            "center_lat": g["center_lat"],
            "center_lon": g["center_lon"],
            "lat_min": g["lat_min"],
            "lat_max": g["lat_max"],
            "lon_min": g["lon_min"],
            "lon_max": g["lon_max"],
            "pSpread": g["pSpread"]
        }
        for g in grid_results
    }

    # 🔸 Firestore 저장
    doc_ref = db.collection("fire_results").document(problem_id)
    doc_ref.set({
        "grids": grids_map,
        "global_feature_importance_top3": global_top3
    })

    return {
        "status": "saved",
        "problem_id": problem_id,
        "grids_saved": len(grids_map),
        "global_top3": global_top3
    }
