import cv2
import mediapipe as mp

from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from bicep_analyzer import BicepAnalyzer
from bicep_form_analyzer import BicepFormAnalyzer
from angle_smoother import AngleSmoother
from workout_session import WorkoutSession
from workout_history import WorkoutHistory


# ============================================================
# BICEP CURL DETECTION
# ============================================================

def run_bicep_detection():

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
        print("Expected location:")
        print(model_path)
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

    analyzer = BicepAnalyzer()

    form_analyzer = BicepFormAnalyzer()


    # ========================================================
    # ANGLE SMOOTHERS
    # ========================================================

    left_smoother = AngleSmoother(
        window_size=7
    )

    right_smoother = AngleSmoother(
        window_size=7
    )


    # ========================================================
    # WORKOUT SESSION
    # ========================================================

    session = WorkoutSession(
        exercise_name="Bicep Curl"
    )


    # ========================================================
    # WORKOUT HISTORY
    # ========================================================

    history = WorkoutHistory()


    # ========================================================
    # CAMERA
    # ========================================================

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print()
        print("ERROR: Could not open camera.")
        print()

        landmarker.close()

        return


    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )


    # ========================================================
    # TIMESTAMP
    # ========================================================

    timestamp_ms = 0


    # ========================================================
    # VISIBILITY THRESHOLD
    # ========================================================

    MIN_VISIBILITY = 0.35


    # ========================================================
    # START MESSAGE
    # ========================================================

    print()
    print("=" * 50)
    print("       FITNOVA BICEP CURL AI COACH")
    print("=" * 50)
    print()
    print("Both arms will be detected automatically.")
    print("Press Q to finish the workout.")
    print()


    # ========================================================
    # MAIN CAMERA LOOP
    # ========================================================

    while True:

        # ====================================================
        # READ FRAME
        # ====================================================

        success, frame = cap.read()

        if not success:

            print(
                "ERROR: Could not read camera frame."
            )

            break


        # ====================================================
        # MIRROR CAMERA
        # ====================================================

        frame = cv2.flip(
            frame,
            1
        )


        height, width, _ = frame.shape


        # ====================================================
        # RGB CONVERSION
        # ====================================================

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # ====================================================
        # MEDIAPIPE IMAGE
        # ====================================================

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )


        # ====================================================
        # POSE DETECTION
        # ====================================================

        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        timestamp_ms += 33


        # ====================================================
        # PERSON DETECTED
        # ====================================================

        if result.pose_landmarks:

            landmarks = result.pose_landmarks[0]


            # =================================================
            # LEFT ARM LANDMARKS
            # =================================================

            left_shoulder = landmarks[11]
            left_elbow = landmarks[13]
            left_wrist = landmarks[15]


            # =================================================
            # RIGHT ARM LANDMARKS
            # =================================================

            right_shoulder = landmarks[12]
            right_elbow = landmarks[14]
            right_wrist = landmarks[16]


            # =================================================
            # VISIBILITY
            # =================================================

            left_visibility = (
                getattr(
                    left_shoulder,
                    "visibility",
                    0.0
                )
                +
                getattr(
                    left_elbow,
                    "visibility",
                    0.0
                )
                +
                getattr(
                    left_wrist,
                    "visibility",
                    0.0
                )
            ) / 3


            right_visibility = (
                getattr(
                    right_shoulder,
                    "visibility",
                    0.0
                )
                +
                getattr(
                    right_elbow,
                    "visibility",
                    0.0
                )
                +
                getattr(
                    right_wrist,
                    "visibility",
                    0.0
                )
            ) / 3


            # =================================================
            # INITIALIZE LEFT VARIABLES
            # =================================================

            left_angle = None

            left_shoulder_point = None
            left_elbow_point = None
            left_wrist_point = None


            # =================================================
            # LEFT ARM DETECTION
            # =================================================

            if left_visibility >= MIN_VISIBILITY:

                left_shoulder_point = (
                    int(left_shoulder.x * width),
                    int(left_shoulder.y * height)
                )

                left_elbow_point = (
                    int(left_elbow.x * width),
                    int(left_elbow.y * height)
                )

                left_wrist_point = (
                    int(left_wrist.x * width),
                    int(left_wrist.y * height)
                )


                # Calculate raw angle

                left_raw_angle = (
                    BicepAnalyzer.calculate_angle(
                        left_shoulder_point,
                        left_elbow_point,
                        left_wrist_point
                    )
                )


                # Smooth angle

                left_angle = left_smoother.update(
                    left_raw_angle
                )


            # =================================================
            # INITIALIZE RIGHT VARIABLES
            # =================================================

            right_angle = None

            right_shoulder_point = None
            right_elbow_point = None
            right_wrist_point = None


            # =================================================
            # RIGHT ARM DETECTION
            # =================================================

            if right_visibility >= MIN_VISIBILITY:

                right_shoulder_point = (
                    int(right_shoulder.x * width),
                    int(right_shoulder.y * height)
                )

                right_elbow_point = (
                    int(right_elbow.x * width),
                    int(right_elbow.y * height)
                )

                right_wrist_point = (
                    int(right_wrist.x * width),
                    int(right_wrist.y * height)
                )


                # Calculate raw angle

                right_raw_angle = (
                    BicepAnalyzer.calculate_angle(
                        right_shoulder_point,
                        right_elbow_point,
                        right_wrist_point
                    )
                )


                # Smooth angle

                right_angle = right_smoother.update(
                    right_raw_angle
                )


            # =================================================
            # REP COUNTER
            # =================================================

            reps, left_state, right_state = (
                analyzer.update(
                    left_angle=left_angle,
                    right_angle=right_angle
                )
            )


            # =================================================
            # FORM ANALYSIS
            # =================================================

            form_score, form_feedback = (
                form_analyzer.analyze(

                    left_angle=left_angle,

                    right_angle=right_angle,

                    left_shoulder=left_shoulder_point,

                    left_elbow=left_elbow_point,

                    left_wrist=left_wrist_point,

                    right_shoulder=right_shoulder_point,

                    right_elbow=right_elbow_point,

                    right_wrist=right_wrist_point
                )
            )


            # =================================================
            # UPDATE WORKOUT SESSION
            # =================================================

            session.update(
                reps=reps,
                form_score=form_score
            )


            # =================================================
            # DRAW LEFT ARM
            # =================================================

            if left_angle is not None:

                cv2.circle(
                    frame,
                    left_shoulder_point,
                    8,
                    (0, 0, 255),
                    -1
                )

                cv2.circle(
                    frame,
                    left_elbow_point,
                    10,
                    (0, 0, 255),
                    -1
                )

                cv2.circle(
                    frame,
                    left_wrist_point,
                    8,
                    (0, 0, 255),
                    -1
                )


                cv2.line(
                    frame,
                    left_shoulder_point,
                    left_elbow_point,
                    (255, 255, 0),
                    3
                )

                cv2.line(
                    frame,
                    left_elbow_point,
                    left_wrist_point,
                    (255, 255, 0),
                    3
                )


                cv2.putText(
                    frame,
                    f"{int(left_angle)}",
                    (
                        left_elbow_point[0] + 15,
                        left_elbow_point[1]
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )


            # =================================================
            # DRAW RIGHT ARM
            # =================================================

            if right_angle is not None:

                cv2.circle(
                    frame,
                    right_shoulder_point,
                    8,
                    (0, 255, 0),
                    -1
                )

                cv2.circle(
                    frame,
                    right_elbow_point,
                    10,
                    (0, 255, 0),
                    -1
                )

                cv2.circle(
                    frame,
                    right_wrist_point,
                    8,
                    (0, 255, 0),
                    -1
                )


                cv2.line(
                    frame,
                    right_shoulder_point,
                    right_elbow_point,
                    (255, 255, 0),
                    3
                )

                cv2.line(
                    frame,
                    right_elbow_point,
                    right_wrist_point,
                    (255, 255, 0),
                    3
                )


                cv2.putText(
                    frame,
                    f"{int(right_angle)}",
                    (
                        right_elbow_point[0] + 15,
                        right_elbow_point[1]
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )


            # =================================================
            # HEADER
            # =================================================

            cv2.putText(
                frame,
                "FITNOVA - BICEP CURL",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2
            )


            # =================================================
            # LEFT STATUS
            # =================================================

            if left_angle is not None:

                left_text = (
                    f"LEFT: {int(left_angle)} deg "
                    f"[{left_state}]"
                )

            else:

                left_text = (
                    "LEFT: Not detected"
                )


            cv2.putText(
                frame,
                left_text,
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )


            # =================================================
            # RIGHT STATUS
            # =================================================

            if right_angle is not None:

                right_text = (
                    f"RIGHT: {int(right_angle)} deg "
                    f"[{right_state}]"
                )

            else:

                right_text = (
                    "RIGHT: Not detected"
                )


            cv2.putText(
                frame,
                right_text,
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )


            # =================================================
            # REPS
            # =================================================

            cv2.putText(
                frame,
                f"REPS: {reps}",
                (20, 155),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.85,
                (255, 255, 255),
                2
            )


            # =================================================
            # FORM SCORE
            # =================================================

            cv2.putText(
                frame,
                f"FORM: {form_score}/100",
                (20, 195),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )


            # =================================================
            # FEEDBACK
            # =================================================

            feedback_y = 235


            for message in form_feedback[:2]:

                cv2.putText(
                    frame,
                    message,
                    (20, feedback_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2
                )

                feedback_y += 30


        # ====================================================
        # NO PERSON
        # ====================================================

        else:

            cv2.putText(
                frame,
                "No person detected",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )


        # ====================================================
        # SHOW FRAME
        # ====================================================

        cv2.imshow(
            "FitNova - Bicep Curl AI Coach",
            frame
        )


        # ====================================================
        # KEYBOARD
        # ====================================================

        key = cv2.waitKey(1) & 0xFF


        if key == ord("q"):

            break


    # ========================================================
    # FINISH WORKOUT
    # ========================================================

    session.finish()


    # ========================================================
    # RELEASE RESOURCES
    # ========================================================

    cap.release()

    cv2.destroyAllWindows()

    landmarker.close()


    # ========================================================
    # GET WORKOUT SUMMARY
    # ========================================================

    summary = session.get_summary()


    # ========================================================
    # SAVE WORKOUT HISTORY
    # ========================================================

    saved = history.add_workout(
        summary
    )


    # ========================================================
    # DISPLAY SUMMARY
    # ========================================================

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


    # ========================================================
    # HISTORY STATUS
    # ========================================================

    if saved:

        print(
            "Workout saved to history."
        )

    else:

        print(
            "Warning: Workout could not be saved."
        )


    print()

    print("=" * 50)
    print()


    input(
        "Press Enter to return to FitNova..."
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    run_bicep_detection()