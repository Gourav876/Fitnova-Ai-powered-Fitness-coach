import math


class PushUpAnalyzer:
    """
    FitNova Push-up Analyzer

    Detects:
        - Push-up repetitions
        - Elbow angle
        - Body alignment
        - Basic form score
        - Real-time feedback
    """

    def __init__(self):

        self.reps = 0

        self.state = "UP"

        self.previous_state = "UP"


    # ========================================================
    # ANGLE CALCULATION
    # ========================================================

    @staticmethod
    def calculate_angle(a, b, c):
        """
        Calculate angle ABC.

        a = first point
        b = middle point
        c = third point
        """

        angle = math.degrees(
            math.atan2(
                c[1] - b[1],
                c[0] - b[0]
            )
            -
            math.atan2(
                a[1] - b[1],
                a[0] - b[0]
            )
        )

        angle = abs(angle)

        if angle > 180:

            angle = 360 - angle

        return angle


    # ========================================================
    # REP COUNTER
    # ========================================================

    def update(self, elbow_angle):

        self.previous_state = self.state


        # ----------------------------------------------------
        # TOP POSITION
        # ----------------------------------------------------

        if elbow_angle >= 155:

            self.state = "UP"


        # ----------------------------------------------------
        # GOING DOWN
        # ----------------------------------------------------

        elif (
            elbow_angle < 155
            and
            elbow_angle > 100
        ):

            if self.state == "UP":

                self.state = "GOING_DOWN"


        # ----------------------------------------------------
        # BOTTOM POSITION
        # ----------------------------------------------------

        elif elbow_angle <= 100:

            self.state = "DOWN"


        # ----------------------------------------------------
        # COUNT REP
        # ----------------------------------------------------

        if (
            self.previous_state == "DOWN"
            and
            self.state == "UP"
        ):

            self.reps += 1


        return self.reps, self.state


    # ========================================================
    # BODY ALIGNMENT
    # ========================================================

    @staticmethod
    def calculate_body_alignment(
        shoulder,
        hip,
        knee,
        ankle
    ):
        """
        Calculate body alignment using
        shoulder → hip → knee → ankle.

        Returns:
            alignment_angle
        """

        # Shoulder → hip vector
        vector1 = (
            shoulder[0] - hip[0],
            shoulder[1] - hip[1]
        )

        # Knee → hip vector
        vector2 = (
            knee[0] - hip[0],
            knee[1] - hip[1]
        )

        angle = math.degrees(
            math.atan2(
                vector2[1],
                vector2[0]
            )
            -
            math.atan2(
                vector1[1],
                vector1[0]
            )
        )

        angle = abs(angle)

        if angle > 180:

            angle = 360 - angle

        return angle


    # ========================================================
    # BODY ALIGNMENT STATUS
    # ========================================================

    def get_alignment_status(
        self,
        shoulder,
        hip,
        knee
    ):
        """
        Estimate whether the hips are aligned
        with the upper and lower body.
        """

        shoulder_y = shoulder[1]

        hip_y = hip[1]

        knee_y = knee[1]


        # ----------------------------------------------------
        # Difference between shoulder and hip
        # ----------------------------------------------------

        upper_difference = abs(
            hip_y - shoulder_y
        )


        # ----------------------------------------------------
        # Difference between hip and knee
        # ----------------------------------------------------

        lower_difference = abs(
            knee_y - hip_y
        )


        # ----------------------------------------------------
        # Avoid division by zero
        # ----------------------------------------------------

        if lower_difference == 0:

            return "GOOD"


        ratio = (
            upper_difference /
            lower_difference
        )


        # ----------------------------------------------------
        # HIPS TOO HIGH
        # ----------------------------------------------------

        if ratio < 0.45:

            return "HIPS_HIGH"


        # ----------------------------------------------------
        # HIPS TOO LOW
        # ----------------------------------------------------

        if ratio > 1.8:

            return "HIPS_LOW"


        return "GOOD"


    # ========================================================
    # FORM SCORE
    # ========================================================

    def get_form_score(
        self,
        elbow_angle,
        alignment_status
    ):

        score = 100


        # ----------------------------------------------------
        # ELBOW FORM
        # ----------------------------------------------------

        if elbow_angle < 70:

            score -= 20

        elif 70 <= elbow_angle < 90:

            score -= 5

        elif 90 <= elbow_angle <= 110:

            score += 0

        elif 110 < elbow_angle < 150:

            score -= 5

        elif elbow_angle >= 170:

            score -= 10


        # ----------------------------------------------------
        # BODY ALIGNMENT
        # ----------------------------------------------------

        if alignment_status == "HIPS_HIGH":

            score -= 20


        elif alignment_status == "HIPS_LOW":

            score -= 20


        return max(
            0,
            min(100, score)
        )


    # ========================================================
    # FEEDBACK
    # ========================================================

    def get_feedback(
        self,
        elbow_angle,
        alignment_status
    ):

        feedback = []


        # ----------------------------------------------------
        # HIP FEEDBACK
        # ----------------------------------------------------

        if alignment_status == "HIPS_HIGH":

            feedback.append(
                "Lower your hips"
            )


        elif alignment_status == "HIPS_LOW":

            feedback.append(
                "Raise your hips"
            )


        # ----------------------------------------------------
        # ELBOW FEEDBACK
        # ----------------------------------------------------

        if elbow_angle < 70:

            feedback.append(
                "Do not go too deep"
            )


        elif 70 <= elbow_angle < 90:

            feedback.append(
                "Almost at good depth"
            )


        elif 90 <= elbow_angle <= 110:

            feedback.append(
                "Good depth"
            )


        elif 110 < elbow_angle < 150:

            feedback.append(
                "Go lower"
            )


        elif elbow_angle >= 170:

            feedback.append(
                "Fully extend your arms"
            )


        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        if not feedback:

            feedback.append(
                "Keep good form"
            )


        return feedback