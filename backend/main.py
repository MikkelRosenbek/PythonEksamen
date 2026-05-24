
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
from . import analysis, plots, llm
import io

app = FastAPI()

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
	df = pd.read_csv(file.file, parse_dates=["date"])
	stats = analysis.calculate_stats(df)
	return JSONResponse(stats)

@app.post("/plot/{plot_type}")
async def plot(plot_type: str, file: UploadFile = File(...)):
	df = pd.read_csv(file.file, parse_dates=["date"])
	if plot_type == "distance":
		img = plots.plot_distance_over_time(df)
	elif plot_type == "speed":
		img = plots.plot_avg_speed_over_time(df)
	else:
		return JSONResponse({"error": "Invalid plot type"}, status_code=400)
	return StreamingResponse(io.BytesIO(img), media_type="image/png")

@app.post("/llm/")
async def llm_feedback(file: UploadFile = File(...)):
	df = pd.read_csv(file.file, parse_dates=["date"])
	stats = analysis.calculate_stats(df)
	feedback = llm.get_llm_feedback(stats)
	return {"feedback": feedback}
