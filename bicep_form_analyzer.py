class BicepFormAnalyzer:

    def __init__(self):

        self.feedback = []

        # Total score = 100
        self.range_score = 40
        self.elbow_score = 30
        self.shoulder_score = 30

        # Previous shoulder positions
        self.previous_left_shoulder = None
        self.previous_right_shoulder = None


    # ============================================================
    # ANALYZE ONE ARM
    # ============================================================

    def analyze_arm(
        self,
        elbow_angle,
        shoulder,
        elbow,
        wrist,
        arm_name
    ):

        feedback = []

        range_score = 40
        elbow_score = 30
        shoulder_score = 30


        # ========================================================
        # 1. RANGE OF MOTION
        # ========================================================

        if elbow_angle <= 80:

            range_score = 40

        elif elbow_angle <= 100:

            range_score = 35

            feedback.append(
                f"{arm_name}: Curl a little higher"
            )

        elif elbow_angle <= 120:

            range_score = 25

            feedback.append(
                f"{arm_name}: Increase your curl range"
            )

        else:

            range_score = 15

            feedback.append(
                f"{arm_name}: Curl your arm more"
            )


        # ========================================================
        # 2. ELBOW POSITION
        # ========================================================

        # Calculate horizontal movement of elbow
        # relative to shoulder.

        horizontal_difference = abs(
            elbow[0] - shoulder[0]
        )


        if horizontal_difference < 80:

            elbow_score = 30

        elif horizontal_difference < 130:

            elbow_score = 22

            feedback.append(
                f"{arm_name}: Keep your elbow closer to your body"
            )

        else:

            elbow_score = 15

            feedback.append(
                f"{arm_name}: Avoid moving your elbow forward"
            )


        # ========================================================
        # 3. SHOULDER POSITION
        # ========================================================

        if arm_name == "LEFT":

            previous_shoulder = (
                self.previous_left_shoulder
            )

            self.previous_left_shoulder = shoulder[1]

        else:

            previous_shoulder = (
                self.previous_right_shoulder
            )

            self.previous_right_shoulder = shoulder[1]


        if previous_shoulder is None:

            shoulder_score = 30

        else:

            shoulder_movement = abs(
                shoulder[1]
                -
                previous_shoulder
            )


            if shoulder_movement < 0.025:

                shoulder_score = 30

            elif shoulder_movement < 0.06:

                shoulder_score = 22

                feedback.append(
                    f"{arm_name}: Keep your shoulder stable"
                )

            else:

                shoulder_score = 15

                feedback.append(
                    f"{arm_name}: Avoid lifting your shoulder"
                )


        # ========================================================
        # TOTAL ARM SCORE
        # ========================================================

        total_score = (
            range_score
            +
            elbow_score
            +
            shoulder_score
        )


        return total_score, feedback


    # ============================================================
    # ANALYZE BOTH ARMS
    # ============================================================

    def analyze(
        self,
        left_angle=None,
        right_angle=None,
        left_shoulder=None,
        left_elbow=None,
        left_wrist=None,
        right_shoulder=None,
        right_elbow=None,
        right_wrist=None
    ):

        self.feedback = []

        scores = []


        # ========================================================
        # LEFT ARM
        # ========================================================

        if (
            left_angle is not None
            and
            left_shoulder is not None
            and
            left_elbow is not None
            and
            left_wrist is not None
        ):

            left_score, left_feedback = (
                self.analyze_arm(
                    left_angle,
                    left_shoulder,
                    left_elbow,
                    left_wrist,
                    "LEFT"
                )
            )

            scores.append(left_score)

            self.feedback.extend(
                left_feedback
            )


        # ========================================================
        # RIGHT ARM
        # ========================================================

        if (
            right_angle is not None
            and
            right_shoulder is not None
            and
            right_elbow is not None
            and
            right_wrist is not None
        ):

            right_score, right_feedback = (
                self.analyze_arm(
                    right_angle,
                    right_shoulder,
                    right_elbow,
                    right_wrist,
                    "RIGHT"
                )
            )

            scores.append(right_score)

            self.feedback.extend(
                right_feedback
            )


        # ========================================================
        # NO ARMS
        # ========================================================

        if not scores:

            return 0, [
                "No arm detected"
            ]


        # ========================================================
        # FINAL SCORE
        # ========================================================

        total_score = int(
            sum(scores) / len(scores)
        )


        # ========================================================
        # POSITIVE FEEDBACK
        # ========================================================

        if total_score >= 90:

            self.feedback.insert(
                0,
                "Excellent form!"
            )

        elif total_score >= 75:

            self.feedback.insert(
                0,
                "Good form"
            )

        elif total_score >= 60:

            self.feedback.insert(
                0,
                "Try to improve your form"
            )

        else:

            self.feedback.insert(
                0,
                "Focus on your technique"
            )


        return total_score, self.feedback