
import requests
from typing import Dict, Any

def get_llm_feedback(stats: Dict[str, Any]) -> str:
	# Placeholder: Her skal du indsætte din LLM API-kald (fx Mistral)
	# Eksempel på prompt
	prompt = (
		f"Du er en AI-cykelcoach. Brugeren har cyklet {stats['num_rides']} ture, "
		f"samlet distance {stats['total_distance']} km, længste tur {stats['longest_ride']} km, "
		f"gennemsnitshastighed {stats['avg_speed']:.1f} km/t. Giv feedback og forslag til næste træning."
	)
	# Her ville du normalt kalde en ekstern LLM API:
	# response = requests.post("https://api.mistral.ai/v1/chat/completions", ...)
	# return response.json()["choices"][0]["message"]["content"]
	# For demo returneres dummy tekst:
	return "Godt kørt! Du har haft en flot udvikling. Prøv en længere tur næste gang og hold øje med din restitution."
