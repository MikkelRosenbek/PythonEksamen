from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
import io

from pydantic import BaseModel, Field

from . import analysis, llm, plots
from .data_store import append_ride, load_data

app = FastAPI()


class RideInput(BaseModel):
    date: str
    distance_km: float = Field(..., gt=0)
    duration_min: float = Field(..., gt=0)
    avg_speed_kmh: float = Field(..., gt=0)
    elevation_m: float = Field(..., ge=0)


@app.get("/rides/")
async def get_rides():
    df = load_data().sort_values("date", ascending=False)
    records: List[dict] = df.assign(
        date=df["date"].dt.strftime("%Y-%m-%d")
    ).to_dict(orient="records")
    return {"rides": records, "csv_path": str(Path("data") / "myData.csv")}


@app.post("/rides/")
async def create_ride(ride: RideInput):
    df = append_ride(ride.model_dump())
    return JSONResponse(
        {
            "message": "Ride saved to data/myData.csv",
            "num_rides": int(df.shape[0]),
        }
    )


@app.get("/analyze/")
async def analyze_data():
    df = load_data()
    stats = analysis.calculate_stats(df)
    return JSONResponse(stats)


@app.get("/plot/{plot_type}")
async def plot(plot_type: str):
    df = load_data()
    if plot_type == "distance":
        img = plots.plot_distance_over_time(df)
    elif plot_type == "speed":
        img = plots.plot_avg_speed_over_time(df)
    else:
        return JSONResponse({"error": "Invalid plot type"}, status_code=400)
    return StreamingResponse(io.BytesIO(img), media_type="image/png")


@app.get("/llm/")
async def llm_feedback():
    df = load_data()
    stats = analysis.calculate_stats(df)
    feedback = llm.get_llm_feedback(stats)
    return {"feedback": feedback}
