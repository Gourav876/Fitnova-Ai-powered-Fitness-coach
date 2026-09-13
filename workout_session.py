import time


class WorkoutSession:
    """
    Tracks a FitNova workout session.

    Stores:
    - Exercise name
    - Total repetitions
    - Form scores
    - Workout duration
    - Best form score
    - Average form score
    - Performance level
    """

    def __init__(self, exercise_name="Squat"):

        # ====================================================
        # EXERCISE
        # ====================================================

        self.exercise_name = exercise_name

        # ====================================================
        # TIME
        # ====================================================

        self.start_time = time.time()
        self.end_time = None

        # ====================================================
        # REPETITIONS
        # ====================================================

        self.total_reps = 0

        # ====================================================
        # FORM SCORES
        # ====================================================

        self.form_scores = []

        # ====================================================
        # BEST FORM
        # ====================================================

        self.best_form_score = 0


    # ========================================================
    # UPDATE SESSION
    # ========================================================

    def update(self, reps, form_score):
        """
        Update workout statistics.
        """

        # ----------------------------------------------------
        # UPDATE REPETITIONS
        # ----------------------------------------------------

        if reps is not None:

            try:

                self.total_reps = int(reps)

            except (TypeError, ValueError):

                pass


        # ----------------------------------------------------
        # UPDATE FORM SCORE
        # ----------------------------------------------------

        if form_score is not None:

            try:

                form_score = float(form_score)

            except (TypeError, ValueError):

                return


            # ------------------------------------------------
            # VALID SCORE
            # ------------------------------------------------

            if 0 <= form_score <= 100:

                self.form_scores.append(
                    form_score
                )


                # ------------------------------------------------
                # UPDATE BEST SCORE
                # ------------------------------------------------

                if form_score > self.best_form_score:

                    self.best_form_score = form_score


    # ========================================================
    # FINISH SESSION
    # ========================================================

    def finish(self):
        """
        Finish the workout session.
        """

        self.end_time = time.time()


    # ========================================================
    # GET DURATION
    # ========================================================

    def get_duration(self):
        """
        Return workout duration in seconds.
        """

        if self.end_time is not None:

            duration = (
                self.end_time
                -
                self.start_time
            )

        else:

            duration = (
                time.time()
                -
                self.start_time
            )

        return max(
            0,
            duration
        )


    # ========================================================
    # GET DURATION TEXT
    # ========================================================

    def get_duration_text(self):
        """
        Return workout duration as MM:SS.
        """

        duration = int(
            self.get_duration()
        )

        minutes = duration // 60

        seconds = duration % 60

        return (
            f"{minutes:02d}:{seconds:02d}"
        )


    # ========================================================
    # AVERAGE FORM SCORE
    # ========================================================

    def get_average_form_score(self):
        """
        Calculate average form score.
        """

        if not self.form_scores:

            return 0


        average = (
            sum(self.form_scores)
            /
            len(self.form_scores)
        )

        return round(
            average,
            1
        )


    # ========================================================
    # PERFORMANCE LEVEL
    # ========================================================

    def get_performance_level(self):
        """
        Determine overall workout performance.
        """

        average = (
            self.get_average_form_score()
        )


        if average >= 90:

            return "Excellent"

        elif average >= 75:

            return "Good"

        elif average >= 60:

            return "Needs Improvement"

        else:

            return "Poor"


    # ========================================================
    # WORKOUT SUMMARY
    # ========================================================

    def get_summary(self):
        """
        Return complete workout summary.
        """

        return {

            "exercise":
                self.exercise_name,

            "reps":
                self.total_reps,

            "best_form":
                self.best_form_score,

            "average_form":
                self.get_average_form_score(),

            "duration":
                self.get_duration_text(),

            "performance":
                self.get_performance_level()
        }


    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    def print_summary(self):
        """
        Display workout summary in terminal.
        """

        summary = self.get_summary()


        print()
        print("=" * 50)
        print("          FITNOVA WORKOUT SUMMARY")
        print("=" * 50)
        print()


        print(
            f"Exercise       : "
            f"{summary['exercise']}"
        )


        print(
            f"Repetitions    : "
            f"{summary['reps']}"
        )


        print(
            f"Best Form      : "
            f"{summary['best_form']}/100"
        )


        print(
            f"Average Form   : "
            f"{summary['average_form']}/100"
        )


        print(
            f"Duration       : "
            f"{summary['duration']}"
        )


        print(
            f"Performance    : "
            f"{summary['performance']}"
        )


        print()
        print("=" * 50)
        print()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    session = WorkoutSession(
        exercise_name="Test Workout"
    )


    # Simulate workout data

    session.update(
        reps=10,
        form_score=85
    )

    session.update(
        reps=10,
        form_score=90
    )

    session.update(
        reps=10,
        form_score=80
    )


    session.finish()


    # Print summary

    session.print_summary()