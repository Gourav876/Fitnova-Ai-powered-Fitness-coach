import cv2
import mediapipe as mp

from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from utils import calculate_angle
from squat_analyzer import SquatAnalyzer
from form_analyzer import SquatFormAnalyzer
from angle_smoother import AngleSmoother
from workout_session import WorkoutSession
from workout_history import WorkoutHistory


def run_squat_detection():

    # ========================================================
    # MODEL PATH
    # ========================================================

    base_dir = Path(__file__).resolve().parent

    model_path = (
        base_dir
        / "models"
        / "pose_landmarker.task"
    )

    # ========================================================
    # CHECK MODEL
    # ========================================================

    if not model_path.exists():

        print()
        print("ERROR: Pose Landmarker model not found.")
        print()
        print(
            f"Expected location:\n{model_path}"
        )
        print()

        return

    # ========================================================
    # MEDIAPIPE SETUP
    # ========================================================

    base_options = python.BaseOptions(
        model_asset_path=str(model_path)
    )

    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1
    )

    landmarker = (
        vision.PoseLandmarker
        .create_from_options(options)
    )

    # ========================================================
    # CREATE ANALYZERS
    # ========================================================

    squat_analyzer = SquatAnalyzer()

    form_analyzer = SquatFormAnalyzer()

    angle_smoother = AngleSmoother(
        window_size=5
    )

    # ========================================================
    # WORKOUT SESSION
    # ========================================================

    workout_session = WorkoutSession(
        exercise_name="Squat"
    )

    # ========================================================
    # WORKOUT HISTORY
    # ========================================================

    workout_history = WorkoutHistory()

    # ========================================================
    # OPEN CAMERA
    # ========================================================

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print()
        print("ERROR: Could not open camera.")
        print()

        landmarker.close()

        return

    # ========================================================
    # START MESSAGE
    # ========================================================

    print()
    print("==========================================")
    print("        FITNOVA SQUAT ANALYZER")
    print("==========================================")
    print()
    print("Camera: ON")
    print()
    print("Stand sideways to the camera.")
    print("Keep your full body visible.")
    print()
    print("Press Q to finish.")
    print()

    # ========================================================
    # TIMESTAMP
    # ========================================================

    timestamp_ms = 0

    # ========================================================
    # CAMERA LOOP
    # ========================================================

    while True:

        success, frame = cap.read()

        if not success:

            print(
                "ERROR: Could not read camera frame."
            )

            break

        # ----------------------------------------------------
        # MIRROR CAMERA
        # ----------------------------------------------------

        frame = cv2.flip(
            frame,
            1
        )

        height, width, _ = frame.shape

        # ----------------------------------------------------
        # CONVERT BGR → RGB
        # ----------------------------------------------------

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ----------------------------------------------------
        # MEDIAPIPE IMAGE
        # ----------------------------------------------------

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # ----------------------------------------------------
        # POSE DETECTION
        # ----------------------------------------------------

        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        timestamp_ms += 33

        # ====================================================
        # PERSON FOUND
        # ====================================================

        if result.pose_landmarks:

            landmarks = result.pose_landmarks[0]

            # ------------------------------------------------
            # LANDMARKS
            # ------------------------------------------------

            shoulder = landmarks[11]

            hip = landmarks[23]

            knee = landmarks[25]

            ankle = landmarks[27]

            # ------------------------------------------------
            # PIXEL COORDINATES
            # ------------------------------------------------

            shoulder_point = (
                int(shoulder.x * width),
                int(shoulder.y * height)
            )

            hip_point = (
                int(hip.x * width),
                int(hip.y * height)
            )

            knee_point = (
                int(knee.x * width),
                int(knee.y * height)
            )

            ankle_point = (
                int(ankle.x * width),
                int(ankle.y * height)
            )

            # ------------------------------------------------
            # RAW KNEE ANGLE
            # ------------------------------------------------

            raw_angle = calculate_angle(
                hip_point,
                knee_point,
                ankle_point
            )

            # ------------------------------------------------
            # SMOOTH ANGLE
            # ------------------------------------------------

            knee_angle = angle_smoother.update(
                raw_angle
            )

            # ------------------------------------------------
            # REP COUNTER
            # ------------------------------------------------

            reps, state = squat_analyzer.update(
                knee_angle
            )

            # ------------------------------------------------
            # FORM ANALYSIS
            # ------------------------------------------------

            form_score, feedback = (
                form_analyzer.analyze(

                    hip=hip_point,

                    knee=knee_point,

                    ankle=ankle_point,

                    shoulder=shoulder_point,

                    knee_angle=knee_angle
                )
            )

            # ------------------------------------------------
            # UPDATE WORKOUT SESSION
            # ------------------------------------------------

            workout_session.update(
                reps=reps,
                form_score=form_score
            )

            # =================================================
            # DRAW LANDMARKS
            # =================================================

            for landmark in landmarks:

                x = int(
                    landmark.x * width
                )

                y = int(
                    landmark.y * height
                )

                if (
                    0 <= x < width
                    and
                    0 <= y < height
                ):

                    cv2.circle(
                        frame,
                        (x, y),
                        4,
                        (0, 255, 0),
                        -1
                    )

            # =================================================
            # IMPORTANT JOINTS
            # =================================================

            cv2.circle(
                frame,
                shoulder_point,
                8,
                (255, 0, 0),
                -1
            )

            cv2.circle(
                frame,
                hip_point,
                8,
                (255, 0, 0),
                -1
            )

            cv2.circle(
                frame,
                knee_point,
                10,
                (0, 0, 255),
                -1
            )

            cv2.circle(
                frame,
                ankle_point,
                8,
                (255, 0, 0),
                -1
            )

            # =================================================
            # BODY LINES
            # =================================================

            cv2.line(
                frame,
                hip_point,
                knee_point,
                (255, 255, 0),
                3
            )

            cv2.line(
                frame,
                knee_point,
                ankle_point,
                (255, 255, 0),
                3
            )

            # =================================================
            # UI
            # =================================================

            cv2.putText(
                frame,
                "FITNOVA - SQUAT",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Knee Angle: {int(knee_angle)} deg",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"State: {state}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Reps: {reps}",
                (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.85,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Form: {form_score}/100",
                (20, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            # ------------------------------------------------
            # FEEDBACK
            # ------------------------------------------------

            if feedback:

                cv2.putText(
                    frame,
                    feedback[0],
                    (20, 230),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

            # ------------------------------------------------
            # INSTRUCTION
            # ------------------------------------------------

            if state == "STANDING":

                instruction = "Start squatting"

            elif state == "GOING_DOWN":

                instruction = "Keep going down"

            elif state == "SQUAT":

                instruction = "Good! Stand up"

            elif state == "GOING_UP":

                instruction = "Stand up completely"

            else:

                instruction = ""

            cv2.putText(
                frame,
                instruction,
                (20, height - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

        # ====================================================
        # NO PERSON
        # ====================================================

        else:

            cv2.putText(
                frame,
                "No person detected",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # ====================================================
        # SHOW WINDOW
        # ====================================================

        cv2.imshow(
            "FitNova - AI Fitness Coach",
            frame
        )

        # ====================================================
        # QUIT
        # ====================================================

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break

    # ========================================================
    # FINISH WORKOUT SESSION
    # ========================================================

    workout_session.finish()

    # ========================================================
    # CLEANUP
    # ========================================================

    cap.release()

    cv2.destroyAllWindows()

    landmarker.close()

    # ========================================================
    # GET WORKOUT SUMMARY
    # ========================================================

    summary = workout_session.get_summary()

    # ========================================================
    # SAVE WORKOUT TO HISTORY
    # ========================================================

    saved = workout_history.add_workout(
        summary
    )

    # ========================================================
    # WORKOUT SUMMARY
    # ========================================================

    print()
    print("==========================================")
    print("         FITNOVA WORKOUT SUMMARY")
    print("==========================================")
    print()

    print(
        f"Exercise       : {summary['exercise']}"
    )

    print(
        f"Total Reps     : {summary['reps']}"
    )

    print(
        f"Best Form      : {summary['best_form']}/100"
    )

    print(
        f"Average Form   : {summary['average_form']}/100"
    )

    print(
        f"Duration       : {summary['duration']}"
    )

    print(
        f"Performance    : {summary['performance']}"
    )

    print()

    # ========================================================
    # SAVE STATUS
    # ========================================================

    if saved:

        print(
            "Workout saved to history."
        )

    else:

        print(
            "WARNING: Workout could not be saved."
        )

    print()

    print("==========================================")


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    run_squat_detection()