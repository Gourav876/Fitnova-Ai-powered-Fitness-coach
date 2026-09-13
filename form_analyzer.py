import math


class SquatFormAnalyzer:

    def __init__(self):

        self.feedback = []

        self.depth_score = 25
        self.torso_score = 25
        self.knee_score = 25
        self.stability_score = 25


    def calculate_angle(self, a, b, c):

        angle = math.degrees(
            math.atan2(c[1] - b[1], c[0] - b[0])
            - math.atan2(a[1] - b[1], a[0] - b[0])
        )

        angle = abs(angle)

        if angle > 180:
            angle = 360 - angle

        return angle


    def analyze(
        self,
        hip,
        knee,
        ankle,
        shoulder,
        knee_angle
    ):

        self.feedback = []

        # Reset scores
        self.depth_score = 25
        self.torso_score = 25
        self.knee_score = 25
        self.stability_score = 25


        # ==================================================
        # 1. DEPTH ANALYSIS
        # ==================================================

        if knee_angle > 120:

            self.depth_score = 10

            self.feedback.append(
                "Go a little deeper"
            )

        elif knee_angle <= 120 and knee_angle > 95:

            self.depth_score = 20

            self.feedback.append(
                "Good depth"
            )

        else:

            self.depth_score = 25

            self.feedback.append(
                "Excellent depth"
            )


        # ==================================================
        # 2. TORSO ANALYSIS
        # ==================================================

        torso_angle = self.calculate_angle(
            shoulder,
            hip,
            knee
        )


        if torso_angle < 60:

            self.torso_score = 15

            self.feedback.append(
                "Keep your chest more upright"
            )

        elif torso_angle < 75:

            self.torso_score = 20

            self.feedback.append(
                "Slightly improve your posture"
            )

        else:

            self.torso_score = 25


        # ==================================================
        # 3. KNEE POSITION
        # ==================================================

        # Compare knee and ankle horizontal positions

        horizontal_difference = abs(
            knee[0] - ankle[0]
        )


        if horizontal_difference > 100:

            self.knee_score = 15

            self.feedback.append(
                "Check your knee alignment"
            )

        elif horizontal_difference > 60:

            self.knee_score = 20

            self.feedback.append(
                "Keep your knee aligned"
            )

        else:

            self.knee_score = 25


        # ==================================================
        # 4. STABILITY
        # ==================================================

        if knee_angle < 70:

            self.stability_score = 20

            self.feedback.append(
                "Avoid going too low"
            )

        else:

            self.stability_score = 25


        # ==================================================
        # 5. TOTAL FORM SCORE
        # ==================================================

        total_score = (
            self.depth_score
            + self.torso_score
            + self.knee_score
            + self.stability_score
        )


        return total_score, self.feedback