import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD .ENV
# ============================================================

load_dotenv()


# ============================================================
# MAIN
# ============================================================

def main():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        print()
        print("ERROR: GEMINI_API_KEY not found.")
        print()
        print("Check your .env file.")
        print()

        return

    print()
    print("=" * 55)
    print("          FITNOVA GEMINI API TEST")
    print("=" * 55)
    print()

    print("API key loaded successfully.")
    print("Connecting to Gemini...")
    print()

    try:

        # ----------------------------------------------------
        # CREATE CLIENT
        # ----------------------------------------------------

        client = genai.Client(
            api_key=api_key
        )

        # ----------------------------------------------------
        # USE INTERACTIONS API
        # ----------------------------------------------------

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=(
                "You are FitNova, an AI fitness coach. "
                "Give me a short friendly greeting."
            )
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        print("Gemini response:")
        print("-" * 55)
        print(interaction.output_text)
        print("-" * 55)
        print()

        print("SUCCESS: Gemini API is working!")
        print()

    except Exception as error:

        print()
        print("ERROR: Gemini API request failed.")
        print()
        print(error)
        print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()