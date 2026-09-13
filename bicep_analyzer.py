import math
import time


class BicepAnalyzer:

    def __init__(self):

        # ========================================================
        # REP COUNT
        # ========================================================

        self.reps = 0

        # ========================================================
        # ARM STATES
        # ========================================================

        self.left_state = "DOWN"
        self.right_state = "DOWN"

        # True when an arm has started a curl
        self.left_started = False
        self.right_started = False

        # ========================================================
        # COMPLETION TIMING
        # ========================================================

        self.left_completed_time = None
        self.right_completed_time = None

        # ========================================================
        # SYNCHRONIZATION WINDOW
        # ========================================================
        #
        # If both arms finish within this amount of time,
        # they are considered ONE repetition.
        #

        self.sync_window = 0.8

        # ========================================================
        # PREVENT REPEATED COUNTING
        # ========================================================

        self.left_counted = False
        self.right_counted = False


    # ============================================================
    # ANGLE CALCULATION
    # ============================================================

    @staticmethod
    def calculate_angle(a, b, c):

        radians = (
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

        angle = abs(
            math.degrees(radians)
        )

        if angle > 180:

            angle = 360 - angle

        return angle


    # ============================================================
    # LEFT ARM
    # ============================================================

    def update_left(self, angle):

        completed = False

        # --------------------------------------------------------
        # START CURL
        # --------------------------------------------------------

        if angle < 100:

            self.left_started = True

            self.left_counted = False

            self.left_state = "UP"


        # --------------------------------------------------------
        # MOVING
        # --------------------------------------------------------

        elif angle < 140:

            if self.left_started:

                self.left_state = "MOVING"

            else:

                self.left_state = "DOWN"


        # --------------------------------------------------------
        # RETURN TO EXTENDED POSITION
        # --------------------------------------------------------

        elif angle >= 140:

            if (
                self.left_started
                and
                not self.left_counted
            ):

                completed = True

                self.left_completed_time = time.time()

                self.left_counted = True

                self.left_started = False


            self.left_state = "DOWN"


        return completed


    # ============================================================
    # RIGHT ARM
    # ============================================================

    def update_right(self, angle):

        completed = False

        # --------------------------------------------------------
        # START CURL
        # --------------------------------------------------------

        if angle < 100:

            self.right_started = True

            self.right_counted = False

            self.right_state = "UP"


        # --------------------------------------------------------
        # MOVING
        # --------------------------------------------------------

        elif angle < 140:

            if self.right_started:

                self.right_state = "MOVING"

            else:

                self.right_state = "DOWN"


        # --------------------------------------------------------
        # RETURN TO EXTENDED POSITION
        # --------------------------------------------------------

        elif angle >= 140:

            if (
                self.right_started
                and
                not self.right_counted
            ):

                completed = True

                self.right_completed_time = time.time()

                self.right_counted = True

                self.right_started = False


            self.right_state = "DOWN"


        return completed


    # ============================================================
    # COUNT REPETITIONS
    # ============================================================

    def process_rep_events(
        self,
        left_completed,
        right_completed
    ):

        now = time.time()


        # ========================================================
        # NOTHING COMPLETED
        # ========================================================

        if (
            not left_completed
            and
            not right_completed
        ):

            return


        # ========================================================
        # BOTH ARMS COMPLETED IN SAME FRAME
        # ========================================================

        if (
            left_completed
            and
            right_completed
        ):

            self.reps += 1

            return


        # ========================================================
        # LEFT ARM COMPLETED
        # ========================================================

        if left_completed:

            # Check whether right arm recently completed

            if (
                self.right_completed_time is not None
                and
                (
                    now
                    -
                    self.right_completed_time
                )
                <= self.sync_window
            ):

                # Same synchronized repetition
                return

            else:

                self.reps += 1

                return


        # ========================================================
        # RIGHT ARM COMPLETED
        # ========================================================

        if right_completed:

            # Check whether left arm recently completed

            if (
                self.left_completed_time is not None
                and
                (
                    now
                    -
                    self.left_completed_time
                )
                <= self.sync_window
            ):

                # Same synchronized repetition
                return

            else:

                self.reps += 1

                return


    # ============================================================
    # UPDATE BOTH ARMS
    # ============================================================

    def update(
        self,
        left_angle=None,
        right_angle=None
    ):

        left_completed = False
        right_completed = False


        # ========================================================
        # LEFT
        # ========================================================

        if left_angle is not None:

            left_completed = self.update_left(
                left_angle
            )


        # ========================================================
        # RIGHT
        # ========================================================

        if right_angle is not None:

            right_completed = self.update_right(
                right_angle
            )


        # ========================================================
        # PROCESS REP EVENTS
        # ========================================================

        self.process_rep_events(
            left_completed,
            right_completed
        )


        return (
            self.reps,
            self.left_state,
            self.right_state
        )


    # ============================================================
    # FORM SCORE
    # ============================================================

    def get_form_score(self, elbow_angle):

        if elbow_angle is None:

            return 0


        if 50 <= elbow_angle <= 80:

            return 100


        elif 80 < elbow_angle <= 100:

            return 90


        elif 100 < elbow_angle < 130:

            return 80


        elif 130 <= elbow_angle <= 165:

            return 95


        elif elbow_angle > 165:

            return 85


        elif elbow_angle < 40:

            return 80


        return 75


    # ============================================================
    # FEEDBACK
    # ============================================================

    def get_feedback(self, elbow_angle):

        if elbow_angle is None:

            return "Arm not detected"


        if elbow_angle >= 165:

            return "Good extension"


        elif elbow_angle >= 140:

            return "Start curling"


        elif elbow_angle >= 120:

            return "Keep curling"


        elif elbow_angle >= 100:

            return "Curl higher"


        elif elbow_angle >= 80:

            return "Almost there"


        elif elbow_angle >= 50:

            return "Good contraction"


        elif elbow_angle >= 40:

            return "Good curl"


        else:

            return "Do not curl too far"