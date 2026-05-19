
import pandas as pd
import numpy as np
from typing import Dict, Any

def load_data(csv_path: str) -> pd.DataFrame:
	df = pd.read_csv(csv_path, parse_dates=["date"])
	return df

def calculate_stats(df: pd.DataFrame) -> Dict[str, Any]:
	stats = {
		"total_distance": float(df["distance_km"].sum()),
		"total_time_min": float(df["duration_min"].sum()),
		"avg_speed": float(df["avg_speed_kmh"].mean()),
		"num_rides": int(df.shape[0]),
		"longest_ride": float(df["distance_km"].max()),
		# "hardest_ride" fjernet, da effort ikke længere bruges
	}
	return stats
