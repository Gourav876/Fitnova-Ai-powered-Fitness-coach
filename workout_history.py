import json
from pathlib import Path
from datetime import datetime


class WorkoutHistory:

    def __init__(self):

        # ========================================================
        # HISTORY FILE
        # ========================================================

        self.file_path = (
            Path(__file__).resolve().parent
            / "workout_history.json"
        )

        # ========================================================
        # LOAD EXISTING HISTORY
        # ========================================================

        self.history = self.load_history()


    # ============================================================
    # LOAD HISTORY
    # ============================================================

    def load_history(self):

        if not self.file_path.exists():

            return []


        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            if isinstance(data, list):

                return data

            return []


        except (
            json.JSONDecodeError,
            OSError
        ):

            return []


    # ============================================================
    # SAVE HISTORY
    # ============================================================

    def save_history(self):

        try:

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.history,
                    file,
                    indent=4
                )

            return True


        except OSError as error:

            print(
                f"Could not save workout history: {error}"
            )

            return False


    # ============================================================
    # ADD WORKOUT
    # ============================================================

    def add_workout(self, summary):

        workout = {

            "date":
                datetime.now().strftime(
                    "%Y-%m-%d"
                ),

            "time":
                datetime.now().strftime(
                    "%H:%M:%S"
                ),

            "exercise":
                summary.get(
                    "exercise",
                    "Unknown"
                ),

            "reps":
                summary.get(
                    "reps",
                    0
                ),

            "best_form":
                summary.get(
                    "best_form",
                    0
                ),

            "average_form":
                summary.get(
                    "average_form",
                    0
                ),

            "duration":
                summary.get(
                    "duration",
                    "00:00"
                ),

            "performance":
                summary.get(
                    "performance",
                    "Unknown"
                )
        }


        self.history.append(
            workout
        )


        return self.save_history()


    # ============================================================
    # GET ALL WORKOUTS
    # ============================================================

    def get_history(self):

        return self.history


    # ============================================================
    # GET RECENT WORKOUTS
    # ============================================================

    def get_recent_workouts(
        self,
        limit=5
    ):

        return self.history[-limit:]


    # ============================================================
    # TOTAL WORKOUTS
    # ============================================================

    def get_total_workouts(self):

        return len(
            self.history
        )


    # ============================================================
    # TOTAL REPS
    # ============================================================

    def get_total_reps(self):

        total = 0

        for workout in self.history:

            total += workout.get(
                "reps",
                0
            )

        return total


    # ============================================================
    # AVERAGE FORM
    # ============================================================

    def get_overall_average_form(self):

        if not self.history:

            return 0


        scores = []

        for workout in self.history:

            score = workout.get(
                "average_form",
                0
            )

            if score > 0:

                scores.append(score)


        if not scores:

            return 0


        return round(
            sum(scores) / len(scores),
            1
        )


    # ============================================================
    # PRINT HISTORY
    # ============================================================

    def print_history(self):

        print()

        print("=" * 65)
        print("                 FITNOVA WORKOUT HISTORY")
        print("=" * 65)

        print()


        if not self.history:

            print(
                "No workouts recorded yet."
            )

            print()

            return


        for index, workout in enumerate(
            self.history,
            start=1
        ):

            print(
                f"{index}. "
                f"{workout.get('date', '-')}"
                f" "
                f"{workout.get('time', '-')}"
            )

            print(
                f"   Exercise    : "
                f"{workout.get('exercise', '-')}"
            )

            print(
                f"   Reps        : "
                f"{workout.get('reps', 0)}"
            )

            print(
                f"   Form        : "
                f"{workout.get('average_form', 0)}/100"
            )

            print(
                f"   Duration    : "
                f"{workout.get('duration', '00:00')}"
            )

            print(
                f"   Performance : "
                f"{workout.get('performance', '-')}"
            )

            print()


        print("=" * 65)


    # ============================================================
    # PRINT PROGRESS
    # ============================================================

    def print_progress(self):

        print()

        print("=" * 50)
        print("                FITNOVA PROGRESS")
        print("=" * 50)

        print()

        print(
            f"Total Workouts : "
            f"{self.get_total_workouts()}"
        )

        print(
            f"Total Reps     : "
            f"{self.get_total_reps()}"
        )

        print(
            f"Average Form   : "
            f"{self.get_overall_average_form()}/100"
        )

        print()

        print("=" * 50)