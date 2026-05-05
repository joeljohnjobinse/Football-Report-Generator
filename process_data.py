def extract_match_stats(match):
    """ Takes one raw match dictionary from the API and returns a clean, structured dictionary."""
    
    date = match["utcDate"][:10]
    competition = match["competition"]["name"]
    home_team = match["homeTeam"]["name"]
    away_team = match["awayTeam"]["name"]
    
    home_score = match["score"]["fullTime"].get("home", 0)
    away_score = match["score"]["fullTime"].get("away", 0)

    if home_score>away_score:
        result = f"{home_team} win"
    elif away_score>home_score:
        result = f"{away_team} win"
    else:
        result = "Draw"

    goals=[]
    raw_goals = match.get("goals", [])

    for goal in raw_goals:
        if not goal.get("scorer") or not goal.get("minute"):
            continue

        goals.append({
            "minute" : goal.get("minute", "?"),
            "scorer" : goal["scorer"].get("name", "Unknown"),
            "team" : goal["team"].get("name", "Unknown"),
            "type" : goal.get("type", "REGULAR")
        })

    bookings = []
    raw_bookings = match.get("bookings", [])

    for bookings in raw_bookings:
        if not bookings.get("player") or not bookings.get("minute"):
            continue

        bookings.append({
            "minute" : bookings.get("minute", "?"),
            "player" : bookings["player"].get("name", "Unknown"),
            "team" : bookings["team"].get("name", "Unknown"),
            "card" : bookings.get("card", "YELLOW")
        })
    
    clean_match = {
        "date": date,
        "competition": competition,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
        "result": result,
        "goals": goals,
        "bookings": bookings
    }

    return clean_match

def format_for_display(clean_match):
    """Takes a clean match dictionary and prints it nicely. Useful for checking your data looks right before moving on."""
    print(f"\n{'='*50}")
    print(f" {clean_match['home_team']} vs {clean_match['away_team']} ")
    print(f" {clean_match['competition']} | {clean_match['date']} ")
    print(f" Final Score:  {clean_match['home_score']} - {clean_match['away_score']}")
    print(f" Result: {clean_match['result']} ")

    print(f"\n Goals: ")
    if clean_match["goals"]:
        for goal in clean_match["goals"]:
            print(f"  {goal['minute']} - {goal['scorer']} ({goal['team']}) [{goal['type']}]")
    else:
        print("  No goals data available.")

    print(f"\n Bookings: ")
    if clean_match["bookings"]:
        for booking in clean_match["bookings"]:
            print(f"  {booking['minute']} - {booking['player']} ({booking['team']}) [{booking['card']}]")
    else:
        print("  No bookings data available.")
    
    print(f"{'='*50}\n")