from fastapi import FastAPI, Request
from firebase_admin import credentials, firestore, initialize_app
from fastapi.responses import JSONResponse
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

@app.post("/reset_input")
def reset_input():
    input_queue.clear()
    return {"status": "queue reset", "length": len(input_queue)}

@app.post("/upload_result")
async def upload_result(request: Request):
    try:
        data = await request.json()

        print("📥 [upload_result] 데이터 수신:", type(data))
        print("📥 내용:", data)

        if not isinstance(data, dict):
            print("❌ 잘못된 데이터 형식:", type(data))
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Expected JSON object (dict), but received something else.",
                    "received_type": str(type(data)),
                    "hint": "loop.m에서 struct 형태로 JSON을 보내야 함"
                }
            )

        problem_id = str(data.get("problem_id", "unknown"))
        print("🔑 문제 ID:", problem_id)

        grid_results = data.get("grid_results", [])
        global_top3 = data.get("global_top3", [])

        print("🧩 격자 수:", len(grid_results))
        print("📊 중요 피처 Top3:", global_top3)

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

        print("🔥 Firestore 저장 준비 완료")

        doc_ref = db.collection("fire_results").document(problem_id)
        doc_ref.set({
            "grids": grids_map,
            "global_feature_importance_top3": global_top3
        })

        print("✅ Firestore 저장 완료")

        return {
            "status": "saved",
            "problem_id": problem_id,
            "grids_saved": len(grids_map),
            "global_top3": global_top3
        }

    except Exception as e:
        print("❗ 예외 발생:", str(e))
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "hint": "FastAPI 로그를 확인하세요"
            }
        )
