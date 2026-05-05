from re import match

import requests
import os
from dotenv import load_dotenv
from process_data import extract_match_stats, format_for_display
from report_generator import generate_report

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://api.football-data.org/v4/"

headers = {
    "X-Auth-Token": API_KEY
}

def get_recent_matches(competition_code="PL", limit=5):
    """
    Fetches recent finished matches from a competition.
    PL = Premier League. You can change this later.
    """
    url = f"{BASE_URL}competitions/{competition_code}/matches"

    params = {
        "status": "FINISHED",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        matches = data["matches"]

        return matches[-limit:]
    else:
        print(f"Error fetching matches: {response.status_code}")
        print(response.text)
        return [] 

def display_match_summary(match):
    """Displays match results in a readable format."""
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    home_score = match["score"]["fullTime"]["home"]
    away_score = match["score"]["fullTime"]["away"]
    date = match["utcDate"][:10]
    print(f"{date}  |  {home} {home_score} - {away_score} {away}")

if __name__ == "__main__":
    print("Fetching recent Premier League matches... \n")
    matches = get_recent_matches("PL", limit=1)

    if matches:
        clean = extract_match_stats(matches[0])
        format_for_display(clean)
        report = generate_report(clean)

        print("MATCH REPORT")
        print("="*50)
        print(report)
        print("="*50)