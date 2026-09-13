from ai_coach import AICoach


class CoachChatbot:

    def __init__(self):

        self.coach = AICoach()

    # ========================================================
    # REFRESH DATA
    # ========================================================

    def refresh(self):

        self.coach.refresh_history()

    # ========================================================
    # ANSWER USER
    # ========================================================

    def respond(self, message):

        self.refresh()

        message = message.lower().strip()

        # ====================================================
        # GREETING
        # ====================================================

        if any(word in message for word in [
            "hello",
            "hi",
            "hey"
        ]):

            return (
                "Hey! I'm your FitNova AI Coach. "
                "I can analyze your workout history, "
                "give you daily feedback, plan your next "
                "workout, recommend sets and reps, and "
                "suggest recipes."
            )

        # ====================================================
        # PROGRESS
        # ====================================================

        if any(word in message for word in [
            "progress",
            "statistics",
            "stats",
            "performance"
        ]):

            stats = self.coach.get_statistics()

            return (
                f"You have completed "
                f"{stats['total_workouts']} workouts.\n\n"
                f"Total reps: {stats['total_reps']}\n"
                f"Average form: {stats['average_form']}/100\n"
                f"Best form: {stats['best_form']}/100"
            )

        # ====================================================
        # LAST WORKOUT
        # ====================================================

        if any(phrase in message for phrase in [
            "last workout",
            "previous workout",
            "yesterday workout",
            "recent workout"
        ]):

            workout = self.coach.get_last_workout()

            if workout is None:

                return (
                    "You don't have any workouts recorded yet."
                )

            return (
                f"Your latest workout was "
                f"{workout.get('exercise', 'Unknown')}.\n\n"
                f"Reps: {workout.get('reps', 0)}\n"
                f"Average form: "
                f"{workout.get('average_form', 0)}/100\n"
                f"Duration: "
                f"{workout.get('duration', '00:00')}\n"
                f"Performance: "
                f"{workout.get('performance', 'Unknown')}"
            )

        # ====================================================
        # DAILY FEEDBACK
        # ====================================================

        if any(phrase in message for phrase in [
            "daily feedback",
            "today feedback",
            "how am i doing",
            "how am i",
            "feedback"
        ]):

            feedback = self.coach.get_daily_feedback()

            return "\n".join(
                f"• {item}"
                for item in feedback
            )

        # ====================================================
        # NEXT WORKOUT
        # ====================================================

        if any(phrase in message for phrase in [
            "next workout",
            "today workout",
            "workout today",
            "what should i do",
            "what should i workout"
        ]):

            plan = self.coach.generate_next_workout()

            response = "Based on your workout history, I recommend:\n\n"

            for item in plan:

                response += (
                    f"🏋️ {item['exercise']}\n"
                    f"Sets: {item['sets']}\n"
                    f"Reps: {item['reps']}\n"
                    f"Reason: {item['reason']}\n\n"
                )

            return response

        # ====================================================
        # SETS / REPS
        # ====================================================

        exercise = None

        if "squat" in message:

            exercise = "Squat"

        elif "push" in message:

            exercise = "Push-up"

        elif (
            "bicep" in message
            or
            "curl" in message
        ):

            exercise = "Bicep Curl"

        if (
            exercise is not None
            and
            (
                "set" in message
                or
                "rep" in message
            )
        ):

            recommendation = (
                self.coach.recommend_sets_reps(
                    exercise
                )
            )

            return (
                f"For {exercise}, I recommend:\n\n"
                f"Sets: {recommendation['sets']}\n"
                f"Reps: {recommendation['reps']}\n\n"
                f"Why: {recommendation['reason']}"
            )

        # ====================================================
        # RECIPES
        # ====================================================

        if any(word in message for word in [
            "recipe",
            "recipes",
            "food",
            "meal",
            "eat"
        ]):

            recipes = self.coach.suggest_recipes()

            response = (
                "Here are some meal ideas:\n\n"
            )

            for recipe in recipes:

                response += (
                    f"🍽️ {recipe['name']}\n"
                    f"Ingredients: "
                    f"{', '.join(recipe['ingredients'])}\n"
                    f"Why: {recipe['reason']}\n\n"
                )

            return response

        # ====================================================
        # HELP
        # ====================================================

        if (
            "help" in message
            or
            "what can you do" in message
        ):

            return (
                "I can help you with:\n\n"
                "• Workout progress\n"
                "• Previous workouts\n"
                "• Daily feedback\n"
                "• Next workout planning\n"
                "• Sets and reps\n"
                "• Squat training\n"
                "• Push-up training\n"
                "• Bicep curl training\n"
                "• Recipe suggestions\n"
            )

        # ====================================================
        # DEFAULT
        # ====================================================

        return (
            "I can help with your workouts, progress, "
            "sets, reps, daily feedback, workout planning, "
            "and recipes.\n\n"
            "Try asking:\n"
            "\"How was my last workout?\"\n"
            "\"What should I do today?\"\n"
            "\"How many sets of squats should I do?\"\n"
            "\"Give me some recipes.\""
        )


# ============================================================
# CHAT INTERFACE
# ============================================================

def run_chatbot():

    chatbot = CoachChatbot()

    print()
    print("=" * 60)
    print("              FITNOVA AI COACH")
    print("=" * 60)
    print()

    print(
        "Your personal AI fitness coach is ready."
    )

    print()

    print(
        "Ask me about your workouts, progress, "
        "sets, reps, recipes, or today's routine."
    )

    print()

    print(
        "Type 'exit' to leave the coach."
    )

    print()

    while True:

        user_message = input(
            "You: "
        ).strip()

        if not user_message:

            continue

        if user_message.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            print()
            print(
                "FitNova Coach: Great work! "
                "See you in your next workout."
            )

            print()

            break

        response = chatbot.respond(
            user_message
        )

        print()

        print(
            "FitNova Coach:"
        )

        print(
            response
        )

        print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_chatbot()