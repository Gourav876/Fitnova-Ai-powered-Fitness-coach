

from pose_detector import run_squat_detection

from pushup_detector import run_pushup_detection

from bicep_detector import run_bicep_detection

from progress import FitnessProgress


# ============================================================
# SHOW PROGRESS
# ============================================================

def show_progress():

    progress = FitnessProgress()

    summary = progress.get_progress_summary()

    print()
    print("==========================================")
    print("           FITNOVA PROGRESS")
    print("==========================================")
    print()

    # --------------------------------------------------------
    # BASIC STATISTICS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # EXERCISE COUNTS
    # --------------------------------------------------------

    print("Workout Count by Exercise")
    print("------------------------------------------")

    exercise_counts = summary["exercise_counts"]

    if exercise_counts:

        for exercise, count in exercise_counts.items():

            print(
                f"{exercise:<20} : {count}"
            )

    else:

        print("No workouts recorded yet.")

    print()

    # --------------------------------------------------------
    # REPS BY EXERCISE
    # --------------------------------------------------------

    print("Total Reps by Exercise")
    print("------------------------------------------")

    reps_by_exercise = summary["reps_by_exercise"]

    if reps_by_exercise:

        for exercise, reps in reps_by_exercise.items():

            print(
                f"{exercise:<20} : {reps}"
            )

    else:

        print("No reps recorded yet.")

    print()

    # --------------------------------------------------------
    # RECENT WORKOUTS
    # --------------------------------------------------------

    print("Recent Workouts")
    print("------------------------------------------")

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

    print("==========================================")
    print()

    input(
        "Press Enter to return to the menu..."
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    while True:

        print()
        print("==========================================")
        print("       FITNOVA AI FITNESS COACH")
        print("==========================================")
        print()

        print("1. Squat")
        print("2. Push-up")
        print("3. Bicep Curl")
        print("4. View Progress")
        print("5. Exit")

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
        # EXIT
        # ====================================================

        elif choice == "5":

            print()
            print("==========================================")
            print("       Thank you for using FitNova!")
            print("==========================================")
            print()

            break

        # ====================================================
        # INVALID OPTION
        # ====================================================

        else:

            print()
            print("Invalid option.")
            print(
                "Please select 1, 2, 3, 4, or 5."
            )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()