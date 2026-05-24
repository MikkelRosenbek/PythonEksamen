
import requests
from typing import Dict, Any


def get_llm_feedback(stats: Dict[str, Any]) -> str:
    # Placeholder indtil en rigtig LLM-provider bliver koblet på projektet.
    prompt = (
        f"Du er en AI-cykelcoach. Brugeren har cyklet {stats['num_rides']} ture, "
        f"samlet distance {stats['total_distance']} km, længste tur {stats['longest_ride']} km, "
        f"gennemsnitshastighed {stats['avg_speed']:.1f} km/t. Giv feedback og forslag til næste træning."
    )
    # Prompten er gemt i variablen allerede nu, så funktionen er let at udvide med et API-kald.
    _ = prompt

    # Her ville du normalt kalde en ekstern LLM API:
    # response = requests.post("https://api.mistral.ai/v1/chat/completions", ...)
    # return response.json()["choices"][0]["message"]["content"]
    return "Godt kørt! Du har haft en flot udvikling. Prøv en længere tur næste gang og hold øje med din restitution."
