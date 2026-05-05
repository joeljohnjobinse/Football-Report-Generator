from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

models_to_try = [
    "openai/gpt-4o-mini",
    "deepseek/deepseek-chat",
    "qwen/qwen-2.5-7b-instruct"
]

def build_prompt(clean_match, tone = "Broadsheet"):
    """ Takes your clean match dictionary and builds a detailed, well-structured prompt for the AI"""
    if clean_match["goals"]:
        goals_text = ""
        for g in clean_match["goals"]:
            goal_type = ""
            if g["type"] == "OWN":
                goal_type = " (own goal)"
            elif g["type"] == "PENALTY":
                goal_type = " (penalty)"
            goals_text += f" - {g['minute']}' : {g['scorer']}  ({g['team']}){goal_type}\n"
    else:
        goals_text = " - Goalscorer data not available\n"
    
    if clean_match["bookings"]:
        bookings_text = ""
        for b in clean_match["bookings"]:
            bookings_text += f" - {b['minute']}' : {b['player']}  ({b['team']}) - {b['card']} card\n"
    else:
        bookings_text = " - No bookings recorded\n"
    
    tone_instructions = {
        "Broadsheet" : "Write in the style of a broadsheet sports journalist — measured, analytical, authoritative.",
        "Pundit" : "Write like a TV football pundit — direct, opinionated, passionate. Use phrases like 'I'll tell you what', 'make no mistake'.",
        "Match day programme": "Write in the warm, celebratory style of a match day programme — enthusiastic about the home side, appreciative of the occasion."
    }

    style_line = tone_instructions.get(tone, tone_instructions["Broadsheet"])

    prompt = f"""You are a professional football journalist writing match reports for a respected sports newspaper.

    Below is the structured match data for a recent game:

    MATCH DETAILS
    ------------
    Competition: {clean_match['competition']},
    Date: {clean_match['date']},
    Home Team: {clean_match['home_team']},
    Away Team: {clean_match['away_team']},
    Score: {clean_match['home_score']} - {clean_match['away_score']},
    Result: {clean_match['result']}

    GOALS
    -----
    {goals_text}

    BOOKINGS
    --------
    {bookings_text}

    INSTRUCTIONS
    ------------
    Write a 3-paragraph match report based strictly on the data above.

    Paragraph 1 - Match summary: who won, the scoreline, and the overal feel of the game.

    Paragraph 2 - Goals: Describe each goal with its minute and scorer. Give each moment weight and drama. If goal data is unavailable, focus on the final result and what it means.

    Paragraph 3 - Wider context: mention any bookings and their impact, what this result means for both teams, and close with a strong final sentence.

    Important rules
    - {style_line}
    - Only use the data provided. Do not make up any details or embellishments.
    - Do not use bullet points or lists. Write in full sentences and paragraphs.
    - Keep the total length to around 200-250 words.
    """

    return prompt

def generate_report(clean_match, tone = "Broadsheet"):
    prompt = build_prompt(clean_match, tone = tone)
    print("Generating match report...\n")

    for model in models_to_try:
        print(f"Trying model: {model}")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )

            report = response.choices[0].message.content

            if report and len(report.strip()) > 50:
                print(f"Success with {model}\n")
                return report
            else:
                print(f"Empty response from {model}, trying next...")

        except Exception as e:
            print(f"Error with model {model}: {e}")
            print("Waiting 3 seconds before trying next...")
            time.sleep(3)
            continue

    return "Report generation failed — all models unavailable. Please try again in a moment."