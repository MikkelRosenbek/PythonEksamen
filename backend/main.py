from __future__ import annotations

import io
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from . import analysis, llm, plots
from .data_store import append_ride, delete_ride, load_data, update_ride


app = FastAPI()


class RideInput(BaseModel):
    date: str
    ride_name: str = Field(..., min_length=1)
    distance_km: float = Field(..., gt=0)
    duration_min: float = Field(..., gt=0)
    avg_speed_kmh: float = Field(..., gt=0)
    elevation_m: float = Field(..., ge=0)


@app.get("/rides/")
async def get_rides():
    # Frontend bruger dette endpoint til at vise alle registrerede ture i tabellen.
    df = load_data().sort_values("date", ascending=False)
    records: List[dict] = df.assign(
        date=df["date"].dt.strftime("%Y-%m-%d")
    ).to_dict(orient="records")
    return {"rides": records, "csv_path": str(Path("data") / "myData.csv")}


@app.post("/rides/")
async def create_ride(ride: RideInput):
    # Gem en ny tur i CSV-filen og returner en enkel bekræftelse til frontend.
    df = append_ride(ride.model_dump())
    return JSONResponse(
        {
            "message": "Ride saved to data/myData.csv",
            "num_rides": int(df.shape[0]),
        }
    )


@app.put("/rides/{ride_id}")
async def edit_ride(ride_id: int, ride: RideInput):
    try:
        df = update_ride(ride_id, ride.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return JSONResponse(
        {
            "message": "Ride updated in data/myData.csv",
            "num_rides": int(df.shape[0]),
        }
    )


@app.delete("/rides/{ride_id}")
async def remove_ride(ride_id: int):
    try:
        df = delete_ride(ride_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return JSONResponse(
        {
            "message": "Ride deleted from data/myData.csv",
            "num_rides": int(df.shape[0]),
        }
    )


@app.get("/analyze/")
async def analyze_data():
    # Statistik læses altid fra den aktuelle CSV-fil, så frontend viser samlet status.
    df = load_data()
    stats = analysis.calculate_stats(df)
    return JSONResponse(stats)


@app.get("/plot/{plot_type}")
async def plot(plot_type: str):
    # Grafer genereres dynamisk fra de seneste data i CSV-filen.
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
    # AI-feedback bygger paa noegletal plus de seneste ture fra CSV-filen.
    df = load_data()
    stats = analysis.calculate_stats(df)
    feedback = llm.get_llm_feedback(stats, df)
    return {"feedback": feedback}
