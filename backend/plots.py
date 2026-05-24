import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

def plot_distance_over_time(df: pd.DataFrame) -> bytes:
	fig, ax = plt.subplots()
	ax.plot(df["date"], df["distance_km"], marker="o")
	ax.set_title("Distance pr. tur")
	ax.set_xlabel("Dato")
	ax.set_ylabel("Distance (km)")
	fig.autofmt_xdate()
	buf = BytesIO()
	plt.savefig(buf, format="png")
	plt.close(fig)
	buf.seek(0)
	return buf.read()

def plot_avg_speed_over_time(df: pd.DataFrame) -> bytes:
	fig, ax = plt.subplots()
	ax.plot(df["date"], df["avg_speed_kmh"], marker="o", color="orange")
	ax.set_title("Gennemsnitshastighed pr. tur")
	ax.set_xlabel("Dato")
	ax.set_ylabel("Hastighed (km/t)")
	fig.autofmt_xdate()
	buf = BytesIO()
	plt.savefig(buf, format="png")
	plt.close(fig)
	buf.seek(0)
	return buf.read()