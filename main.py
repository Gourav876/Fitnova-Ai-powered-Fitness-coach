from exercise_selector import ExerciseSelector

from pose_detector import run_squat_detection

from pushup_detector import run_pushup_detection

from bicep_detector import run_bicep_detection

from progress import FitnessProgress

from ai_coach import AICoach


# ============================================================
# SHOW PROGRESS
# ============================================================

def show_progress():

    progress = FitnessProgress()

    summary = progress.get_progress_summary()

    print()
    print("=" * 50)
    print("           FITNOVA PROGRESS")
    print("=" * 50)
    print()

    # ========================================================
    # BASIC STATISTICS
    # ========================================================

    print(
        f"Total Workouts : "
        f"{summary['total_workouts']}"
    )

    print(
        f"Total Reps     : "
        f"{summary['total_reps']}"
    )

    print(
        f"Average Form   : "
        f"{summary['average_form']}/100"
    )

    print(
        f"Best Form      : "
        f"{summary['best_form']}/100"
    )

    print()

    # ========================================================
    # EXERCISE COUNTS
    # ========================================================

    print("Workout Count by Exercise")
    print("-" * 50)

    exercise_counts = summary["exercise_counts"]

    if exercise_counts:

        for exercise, count in exercise_counts.items():

            print(
                f"{exercise:<20} : {count}"
            )

    else:

        print("No workouts recorded yet.")

    print()

    # ========================================================
    # REPS BY EXERCISE
    # ========================================================

    print("Total Reps by Exercise")
    print("-" * 50)

    reps_by_exercise = summary["reps_by_exercise"]

    if reps_by_exercise:

        for exercise, reps in reps_by_exercise.items():

            print(
                f"{exercise:<20} : {reps}"
            )

    else:

        print("No reps recorded yet.")

    print()

    # ========================================================
    # RECENT WORKOUTS
    # ========================================================

    print("Recent Workouts")
    print("-" * 50)

    recent_workouts = summary["recent_workouts"]

    if recent_workouts:

        for index, workout in enumerate(
            recent_workouts,
            start=1
        ):

            exercise = workout.get(
                "exercise",
                "Unknown"
            )

            reps = workout.get(
                "reps",
                0
            )

            average_form = workout.get(
                "average_form",
                0
            )

            duration = workout.get(
                "duration",
                "00:00"
            )

            print(
                f"{index}. "
                f"{exercise} | "
                f"Reps: {reps} | "
                f"Form: {average_form}/100 | "
                f"Time: {duration}"
            )

    else:

        print("No recent workouts.")

    print()

    print("=" * 50)
    print()

    input(
        "Press Enter to return to the menu..."
    )


# ============================================================
# AI COACH
# ============================================================

def run_ai_coach():

    """
    Start the FitNova AI Coach.

    The AI Coach has access to the user's
    workout history through AICoach.
    """

    coach = AICoach()

    print()
    print("=" * 60)
    print("                 FITNOVA AI COACH")
    print("=" * 60)
    print()

    print(
        "Your personal AI fitness coach is ready."
    )

    print()

    print("You can ask things like:")

    print(
        "• How am I progressing?"
    )

    print(
        "• How was my last workout?"
    )

    print(
        "• What should I train today?"
    )

    print(
        "• How many sets and reps should I do?"
    )

    print(
        "• Suggest a workout for me."
    )

    print(
        "• What should I eat after my workout?"
    )

    print(
        "• Suggest some healthy recipes."
    )

    print()

    print(
        "Type 'exit' to return to the main menu."
    )

    print()

    # ========================================================
    # CHAT LOOP
    # ========================================================

    while True:

        try:

            question = input(
                "You: "
            ).strip()

        except KeyboardInterrupt:

            print()
            print(
                "Returning to FitNova..."
            )
            print()

            break

        except EOFError:

            print()
            print(
                "Returning to FitNova..."
            )
            print()

            break

        # ====================================================
        # EMPTY QUESTION
        # ====================================================

        if not question:

            continue

        # ====================================================
        # EXIT AI COACH
        # ====================================================

        if question.lower() in [
            "exit",
            "quit",
            "back",
            "menu"
        ]:

            print()
            print(
                "FitNova Coach: "
                "Great work! Keep training consistently."
            )

            print()

            break

        # ====================================================
        # SEND QUESTION TO AI
        # ====================================================

        print()

        print(
            "FitNova Coach: Thinking..."
        )

        print()

        answer = coach.ask(
            question
        )

        print(
            "FitNova Coach:"
        )

        print()

        print(
            answer
        )

        print()

        print("-" * 60)

        print()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    while True:

        print()
        print("=" * 50)
        print("       FITNOVA AI FITNESS COACH")
        print("=" * 50)
        print()

        print("1. Squat")
        print("2. Push-up")
        print("3. Bicep Curl")
        print("4. View Progress")
        print("5. AI Coach")
        print("6. Exit")

        print()

        choice = input(
            "Select an option: "
        ).strip()

        # ====================================================
        # SQUAT
        # ====================================================

        if choice == "1":

            print()
            print(
                "Starting FitNova Squat Analyzer..."
            )
            print()

            run_squat_detection()

        # ====================================================
        # PUSH-UP
        # ====================================================

        elif choice == "2":

            print()
            print(
                "Starting FitNova Push-up Analyzer..."
            )
            print()

            run_pushup_detection()

        # ====================================================
        # BICEP CURL
        # ====================================================

        elif choice == "3":

            print()
            print(
                "Starting FitNova Bicep Curl Analyzer..."
            )
            print()

            run_bicep_detection()

        # ====================================================
        # PROGRESS
        # ====================================================

        elif choice == "4":

            show_progress()

        # ====================================================
        # AI COACH
        # ====================================================

        elif choice == "5":

            run_ai_coach()

        # ====================================================
        # EXIT
        # ====================================================

        elif choice == "6":

            print()
            print("=" * 50)
            print(
                "       Thank you for using FitNova!"
            )
            print("=" * 50)
            print()

            break

        # ====================================================
        # INVALID OPTION
        # ====================================================

        else:

            print()

            print(
                "Invalid option."
            )

            print(
                "Please select 1, 2, 3, 4, 5, or 6."
            )

            print()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()