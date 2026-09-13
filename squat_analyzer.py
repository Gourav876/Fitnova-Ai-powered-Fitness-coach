class SquatAnalyzer:

    def __init__(self):

        # Number of completed squats
        self.reps = 0

        # Current movement state
        self.state = "STANDING"

        # Angle thresholds
        self.standing_angle = 160
        self.squat_angle = 110


    def update(self, knee_angle):

        """
        Update squat state using the knee angle.

        Standing:
            angle > 160

        Squat:
            angle < 110

        A repetition is counted when the user:
            1. Starts standing
            2. Goes down
            3. Reaches squat position
            4. Returns to standing
        """


        # -----------------------------------------
        # STANDING → GOING DOWN
        # -----------------------------------------

        if self.state == "STANDING":

            if knee_angle < self.standing_angle:

                self.state = "GOING_DOWN"


        # -----------------------------------------
        # GOING DOWN → SQUAT
        # -----------------------------------------

        elif self.state == "GOING_DOWN":

            if knee_angle < self.squat_angle:

                self.state = "SQUAT"


        # -----------------------------------------
        # SQUAT → GOING UP
        # -----------------------------------------

        elif self.state == "SQUAT":

            if knee_angle > self.squat_angle:

                self.state = "GOING_UP"


        # -----------------------------------------
        # GOING UP → STANDING
        # -----------------------------------------

        elif self.state == "GOING_UP":

            if knee_angle > self.standing_angle:

                self.state = "STANDING"

                # One complete squat!
                self.reps += 1


        return self.reps, self.state