from datetime import datetime

@app.post("/upload_result")
async def upload_result(request: Request):
    try:
        data = await request.json()

        if not isinstance(data, dict):
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Expected JSON object (dict), but received something else.",
                    "hint": "loop.m에서 struct 형태로 JSON을 보내야 함"
                }
            )

        grid_results = data.get("grid_results", [])
        global_top3 = data.get("global_top3", [])

        # 🔹 격자 결과 구성
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

        # 🔹 시간 기반 문서 ID 생성 (예: 20250714_215803)
        doc_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 🔹 Firestore에 저장
        db.collection("fire_results").document(doc_id).set({
            "timestamp": doc_id,  # 예측 시간도 저장
            "grids": grids_map,
            "global_feature_importance_top3": global_top3
        })

        print(f"✅ 저장 완료: 문서 ID = {doc_id}")

        return {
            "status": "saved",
            "doc_id": doc_id,
            "grids_saved": len(grids_map),
            "global_top3": global_top3
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "hint": "FastAPI 로그를 확인하세요"
            }
        )
