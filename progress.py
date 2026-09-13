from workout_history import WorkoutHistory


class FitnessProgress:

    def __init__(self):

        # ====================================================
        # WORKOUT HISTORY
        # ====================================================

        self.history_manager = WorkoutHistory()

    # ========================================================
    # GET HISTORY
    # ========================================================

    def get_history(self):

        return self.history_manager.get_history()

    # ========================================================
    # TOTAL WORKOUTS
    # ========================================================

    def get_total_workouts(self):

        return self.history_manager.get_total_workouts()

    # ========================================================
    # TOTAL REPS
    # ========================================================

    def get_total_reps(self):

        return self.history_manager.get_total_reps()

    # ========================================================
    # AVERAGE FORM
    # ========================================================

    def get_average_form(self):

        return self.history_manager.get_overall_average_form()

    # ========================================================
    # BEST FORM
    # ========================================================

    def get_best_form(self):

        history = self.get_history()

        if not history:

            return 0

        best_score = 0

        for workout in history:

            score = workout.get(
                "best_form",
                0
            )

            try:

                score = float(score)

            except (
                TypeError,
                ValueError
            ):

                continue

            if score > best_score:

                best_score = score

        return best_score

    # ========================================================
    # EXERCISE COUNTS
    # ========================================================

    def get_exercise_counts(self):

        history = self.get_history()

        counts = {}

        for workout in history:

            exercise = workout.get(
                "exercise",
                "Unknown"
            )

            if exercise not in counts:

                counts[exercise] = 0

            counts[exercise] += 1

        return counts

    # ========================================================
    # REPS BY EXERCISE
    # ========================================================

    def get_reps_by_exercise(self):

        history = self.get_history()

        reps_by_exercise = {}

        for workout in history:

            exercise = workout.get(
                "exercise",
                "Unknown"
            )

            reps = workout.get(
                "reps",
                0
            )

            try:

                reps = int(reps)

            except (
                TypeError,
                ValueError
            ):

                reps = 0

            if exercise not in reps_by_exercise:

                reps_by_exercise[exercise] = 0

            reps_by_exercise[exercise] += reps

        return reps_by_exercise

    # ========================================================
    # RECENT WORKOUTS
    # ========================================================

    def get_recent_workouts(
        self,
        limit=5
    ):

        return self.history_manager.get_recent_workouts(
            limit
        )

    # ========================================================
    # COMPLETE PROGRESS SUMMARY
    # ========================================================

    def get_progress_summary(self):

        return {

            "total_workouts":
                self.get_total_workouts(),

            "total_reps":
                self.get_total_reps(),

            "average_form":
                self.get_average_form(),

            "best_form":
                self.get_best_form(),

            "exercise_counts":
                self.get_exercise_counts(),

            "reps_by_exercise":
                self.get_reps_by_exercise(),

            "recent_workouts":
                self.get_recent_workouts()
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    progress = FitnessProgress()

    summary = progress.get_progress_summary()

    print()
    print("==========================================")
    print("          FITNOVA PROGRESS")
    print("==========================================")
    print()

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

    print("Exercise Counts")
    print("------------------------------------------")

    if summary["exercise_counts"]:

        for exercise, count in (
            summary["exercise_counts"].items()
        ):

            print(
                f"{exercise:<20} : {count}"
            )

    else:

        print("No workouts recorded yet.")

    print()

    print("Reps by Exercise")
    print("------------------------------------------")

    if summary["reps_by_exercise"]:

        for exercise, reps in (
            summary["reps_by_exercise"].items()
        ):

            print(
                f"{exercise:<20} : {reps}"
            )

    else:

        print("No reps recorded yet.")

    print()

    print("==========================================")