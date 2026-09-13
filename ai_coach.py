import os
import json
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from workout_history import WorkoutHistory


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# CHECK API KEY
# ============================================================

if not GEMINI_API_KEY:

    raise RuntimeError(
        "GEMINI_API_KEY not found.\n\n"
        "Make sure your .env file contains:\n"
        "GEMINI_API_KEY=your_api_key"
    )


print("Gemini API key loaded successfully.")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# GEMINI MODEL
# ============================================================

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# AI COACH
# ============================================================

class AICoach:

    """
    FitNova AI Fitness Coach

    Uses workout history to:

    - Analyze previous workouts
    - Give personalized feedback
    - Recommend sets and reps
    - Plan the next workout
    - Adapt workouts based on performance
    - Suggest exercises
    - Suggest recipes
    - Answer fitness questions
    """


    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        self.history_manager = WorkoutHistory()

        self.history = (
            self.history_manager.get_history()
        )


    # ========================================================
    # REFRESH HISTORY
    # ========================================================

    def refresh_history(self):

        self.history_manager = WorkoutHistory()

        self.history = (
            self.history_manager.get_history()
        )


    # ========================================================
    # GET STATISTICS
    # ========================================================

    def get_statistics(self):

        self.refresh_history()

        if not self.history:

            return {
                "total_workouts": 0,
                "total_reps": 0,
                "average_form": 0,
                "best_form": 0
            }


        total_workouts = len(
            self.history
        )

        total_reps = 0

        form_scores = []

        best_form = 0


        for workout in self.history:

            total_reps += workout.get(
                "reps",
                0
            )

            form = workout.get(
                "average_form",
                0
            )

            if form > 0:

                form_scores.append(
                    form
                )

                best_form = max(
                    best_form,
                    form
                )


        if form_scores:

            average_form = round(
                sum(form_scores)
                /
                len(form_scores),
                1
            )

        else:

            average_form = 0


        return {
            "total_workouts":
                total_workouts,

            "total_reps":
                total_reps,

            "average_form":
                average_form,

            "best_form":
                best_form
        }


    # ========================================================
    # RECENT WORKOUTS
    # ========================================================

    def get_recent_workouts(
        self,
        limit=10
    ):

        self.refresh_history()

        return self.history[-limit:]


    # ========================================================
    # LAST WORKOUT
    # ========================================================

    def get_last_workout(self):

        self.refresh_history()

        if not self.history:

            return None

        return self.history[-1]


    # ========================================================
    # BUILD COACH CONTEXT
    # ========================================================

    def build_context(self):

        self.refresh_history()

        statistics = (
            self.get_statistics()
        )

        recent_workouts = (
            self.get_recent_workouts(10)
        )


        context = {

            "date":
                datetime.now().strftime(
                    "%Y-%m-%d"
                ),

            "statistics":
                statistics,

            "recent_workouts":
                recent_workouts
        }


        return context


    # ========================================================
    # ASK GEMINI AI COACH
    # ========================================================

    def ask(self, user_message):

        context = self.build_context()


        # ====================================================
        # SYSTEM INSTRUCTIONS
        # ====================================================

        system_prompt = """

You are FitNova AI Coach.

You are a friendly, encouraging, intelligent and
practical AI fitness coach.

You have access to the user's FitNova workout history.

Your job is to act like a PERSONAL FITNESS COACH.

============================================================
YOUR RESPONSIBILITIES
============================================================

1. Analyze the user's workout history.

2. Give personalized feedback based on actual data.

3. Track improvement over time.

4. Identify weak areas in the user's training.

5. Recommend exercises.

6. Recommend sets and repetitions.

7. Adapt future workouts based on previous performance.

8. Recommend recovery when appropriate.

9. Suggest general healthy recipes and meal ideas.

10. Explain exercise technique.

11. Motivate the user.

12. Help the user stay consistent.

============================================================
WORKOUT RECOMMENDATIONS
============================================================

Whenever you recommend an exercise, clearly mention:

Exercise:
Sets:
Repetitions:
Reason:

Example:

Squat
Sets: 3
Repetitions: 10
Reason: Your recent form has been consistent, so
we can gradually increase training volume.

============================================================
ADAPTIVE TRAINING
============================================================

Use the workout history to adapt the next routine.

If the user's form is improving:

- Gradually increase volume or repetitions.

If form is getting worse:

- Reduce intensity.
- Focus on technique.
- Recommend recovery.

If the user has not trained recently:

- Recommend a manageable session.

Do not suddenly recommend excessive volume.

============================================================
WORKOUT HISTORY
============================================================

Always use the actual workout data provided.

Never invent:

- workout counts
- repetitions
- form scores
- workout dates
- personal records

If there is not enough data, clearly say so.

============================================================
DAILY FEEDBACK
============================================================

When asked for daily feedback:

1. Review recent workouts.
2. Identify progress.
3. Mention strengths.
4. Mention areas to improve.
5. Give practical advice.
6. Recommend the next workout.

============================================================
RECIPES
============================================================

You can suggest practical general healthy meals.

For recipes provide:

Recipe name
Ingredients
Simple preparation
Why it can fit an active lifestyle

Do not claim that a recipe treats a medical condition.

If the user provides dietary restrictions,
respect them.

============================================================
SAFETY
============================================================

Do not diagnose medical conditions.

If the user reports serious pain, injury,
dizziness, chest pain, or other concerning symptoms,
recommend stopping exercise and seeking appropriate
medical advice.

============================================================
COMMUNICATION STYLE
============================================================

Be conversational.

Do not sound like a robot.

Keep answers easy to understand.

Use headings and bullet points when useful.

Be encouraging but honest.

Do not exaggerate progress.

"""


        # ====================================================
        # USER CONTEXT
        # ====================================================

        user_prompt = f"""

USER'S FITNOVA WORKOUT DATA
===========================

{json.dumps(context, indent=2)}


USER'S QUESTION
===============

{user_message}


Using the workout data above, answer the user's
question as their personal FitNova AI Coach.

Remember:

- Use actual workout history.
- Personalize the response.
- Do not invent data.
- Include sets and reps when recommending exercises.
- Adapt recommendations based on previous performance.
"""


        # ====================================================
        # SEND REQUEST TO GEMINI
        # ====================================================

        try:

            response = client.models.generate_content(

                model=MODEL_NAME,

                contents=user_prompt,

                config={
                    "system_instruction": system_prompt
                }
            )


            # =================================================
            # GET RESPONSE TEXT
            # =================================================

            if response.text:

                return response.text


            return (
                "FitNova Coach could not generate "
                "a response right now."
            )


        except Exception as error:

            return (
                "Sorry, I couldn't connect to the "
                "FitNova AI Coach right now.\n\n"
                f"Error: {error}"
            )


# ============================================================
# TEST AI COACH
# ============================================================

def main():

    coach = AICoach()


    print()
    print("=" * 60)
    print("              FITNOVA AI COACH")
    print("=" * 60)
    print()

    print(
        "Your Gemini-powered AI fitness coach is ready."
    )

    print(
        "Ask me anything about your workouts."
    )

    print(
        "Type 'exit' to quit."
    )

    print()


    # ========================================================
    # CHAT LOOP
    # ========================================================

    while True:

        question = input(
            "You: "
        ).strip()


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if question.lower() in [
            "exit",
            "quit"
        ]:

            print()

            print(
                "FitNova Coach: "
                "Great work! Keep training consistently. 💪"
            )

            print()

            break


        # ----------------------------------------------------
        # EMPTY MESSAGE
        # ----------------------------------------------------

        if not question:

            continue


        # ----------------------------------------------------
        # THINKING
        # ----------------------------------------------------

        print()

        print(
            "FitNova Coach: Thinking..."
        )


        # ----------------------------------------------------
        # ASK GEMINI
        # ----------------------------------------------------

        answer = coach.ask(
            question
        )


        # ----------------------------------------------------
        # DISPLAY ANSWER
        # ----------------------------------------------------

        print()

        print(
            "FitNova Coach:"
        )

        print(
            "-" * 60
        )

        print(
            answer
        )

        print(
            "-" * 60
        )

        print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()