import cv2
import mediapipe as mp

from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from pushup_analyzer import PushUpAnalyzer
from angle_smoother import AngleSmoother
from workout_session import WorkoutSession
from workout_history import WorkoutHistory


# ============================================================
# LANDMARK VISIBILITY
# ============================================================

def get_landmark_visibility(landmarks, indexes):
    """
    Calculate the average visibility of selected landmarks.
    """

    visibility_values = []

    for index in indexes:

        visibility = getattr(
            landmarks[index],
            "visibility",
            0.0
        )

        visibility_values.append(
            visibility
        )

    if not visibility_values:

        return 0.0

    return sum(
        visibility_values
    ) / len(
        visibility_values
    )


# ============================================================
# MAIN PUSH-UP DETECTOR
# ============================================================

def run_pushup_detection():

    # ========================================================
    # 1. MODEL PATH
    # ========================================================

    base_dir = Path(__file__).resolve().parent

    model_path = (
        base_dir
        / "models"
        / "pose_landmarker.task"
    )

    # ========================================================
    # 2. CHECK MODEL
    # ========================================================

    if not model_path.exists():

        print()
        print(
            "ERROR: Pose Landmarker model not found."
        )
        print()
        print("Expected location:")
        print(model_path)
        print()

        return

    # ========================================================
    # 3. MEDIAPIPE SETUP
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
    # 4. CREATE ANALYZERS
    # ========================================================

    pushup_analyzer = PushUpAnalyzer()

    angle_smoother = AngleSmoother(
        window_size=5
    )

    # ========================================================
    # 5. WORKOUT SESSION
    # ========================================================

    workout_session = WorkoutSession(
        exercise_name="Push-up"
    )

    # ========================================================
    # 6. WORKOUT HISTORY
    # ========================================================

    workout_history = WorkoutHistory()

    # ========================================================
    # 7. OPEN CAMERA
    # ========================================================

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print()
        print(
            "ERROR: Could not open camera."
        )
        print()

        landmarker.close()

        return

    # ========================================================
    # CAMERA RESOLUTION
    # ========================================================

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )

    # ========================================================
    # SIDE DETECTION VARIABLES
    # ========================================================

    locked_side = None

    side_detection_frames = 0

    REQUIRED_FRAMES = 15

    VISIBILITY_THRESHOLD = 0.45

    # ========================================================
    # START MESSAGE
    # ========================================================

    print()
    print("==========================================")
    print("       FITNOVA PUSH-UP ANALYZER")
    print("==========================================")
    print()
    print("Camera : ON")
    print()
    print("Instructions:")
    print("1. Position yourself sideways.")
    print("2. Keep your complete body visible.")
    print("3. Keep your arm visible.")
    print("4. Wait for FitNova to detect your side.")
    print("5. Perform your push-ups.")
    print("6. Press Q to finish.")
    print()

    # ========================================================
    # TIMESTAMP
    # ========================================================

    timestamp_ms = 0

    # ========================================================
    # CAMERA LOOP
    # ========================================================

    while True:

        # ----------------------------------------------------
        # READ CAMERA
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # FRAME SIZE
        # ----------------------------------------------------

        height, width, _ = frame.shape

        # ----------------------------------------------------
        # BGR → RGB
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
            # LANDMARK GROUPS
            # =================================================

            left_indexes = [
                11,  # left shoulder
                13,  # left elbow
                15,  # left wrist
                23,  # left hip
                25,  # left knee
                27   # left ankle
            ]

            right_indexes = [
                12,  # right shoulder
                14,  # right elbow
                16,  # right wrist
                24,  # right hip
                26,  # right knee
                28   # right ankle
            ]

            # =================================================
            # CALCULATE VISIBILITY
            # =================================================

            left_visibility = (
                get_landmark_visibility(
                    landmarks,
                    left_indexes
                )
            )

            right_visibility = (
                get_landmark_visibility(
                    landmarks,
                    right_indexes
                )
            )

            # =================================================
            # DETECT SIDE
            # =================================================

            if locked_side is None:

                if (
                    left_visibility >=
                    VISIBILITY_THRESHOLD
                    or
                    right_visibility >=
                    VISIBILITY_THRESHOLD
                ):

                    if (
                        left_visibility >=
                        right_visibility
                    ):

                        detected_side = "LEFT"

                    else:

                        detected_side = "RIGHT"

                    side_detection_frames += 1

                    # -----------------------------------------
                    # LOCK SIDE
                    # -----------------------------------------

                    if (
                        side_detection_frames
                        >= REQUIRED_FRAMES
                    ):

                        locked_side = detected_side

                else:

                    side_detection_frames = 0

                    detected_side = None

            else:

                detected_side = locked_side

            # =================================================
            # SELECT LANDMARK INDICES
            # =================================================

            if detected_side == "LEFT":

                shoulder_index = 11
                elbow_index = 13
                wrist_index = 15

                hip_index = 23
                knee_index = 25
                ankle_index = 27

            elif detected_side == "RIGHT":

                shoulder_index = 12
                elbow_index = 14
                wrist_index = 16

                hip_index = 24
                knee_index = 26
                ankle_index = 28

            else:

                shoulder_index = None
                elbow_index = None
                wrist_index = None

                hip_index = None
                knee_index = None
                ankle_index = None

            # =================================================
            # ANALYZE ONLY AFTER SIDE DETECTED
            # =================================================

            if detected_side is not None:

                shoulder = landmarks[
                    shoulder_index
                ]

                elbow = landmarks[
                    elbow_index
                ]

                wrist = landmarks[
                    wrist_index
                ]

                hip = landmarks[
                    hip_index
                ]

                knee = landmarks[
                    knee_index
                ]

                ankle = landmarks[
                    ankle_index
                ]

                # =================================================
                # CONVERT LANDMARKS TO PIXELS
                # =================================================

                shoulder_point = (
                    int(shoulder.x * width),
                    int(shoulder.y * height)
                )

                elbow_point = (
                    int(elbow.x * width),
                    int(elbow.y * height)
                )

                wrist_point = (
                    int(wrist.x * width),
                    int(wrist.y * height)
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

                # =================================================
                # ELBOW ANGLE
                # =================================================

                raw_elbow_angle = (
                    PushUpAnalyzer.calculate_angle(
                        shoulder_point,
                        elbow_point,
                        wrist_point
                    )
                )

                # =================================================
                # SMOOTH ANGLE
                # =================================================

                elbow_angle = (
                    angle_smoother.update(
                        raw_elbow_angle
                    )
                )

                # =================================================
                # REP COUNT
                # =================================================

                reps, state = (
                    pushup_analyzer.update(
                        elbow_angle
                    )
                )

                # =================================================
                # BODY ALIGNMENT
                # =================================================

                alignment_status = (
                    pushup_analyzer.get_alignment_status(
                        shoulder=shoulder_point,
                        hip=hip_point,
                        knee=knee_point
                    )
                )

                # =================================================
                # FORM SCORE
                # =================================================

                form_score = (
                    pushup_analyzer.get_form_score(
                        elbow_angle=elbow_angle,
                        alignment_status=alignment_status
                    )
                )

                # =================================================
                # FEEDBACK
                # =================================================

                feedback_list = (
                    pushup_analyzer.get_feedback(
                        elbow_angle=elbow_angle,
                        alignment_status=alignment_status
                    )
                )

                if feedback_list:

                    feedback = feedback_list[0]

                else:

                    feedback = "Keep good form"

                # =================================================
                # WORKOUT SESSION
                # =================================================

                workout_session.update(
                    reps=reps,
                    form_score=form_score
                )

                # =================================================
                # DRAW ALL LANDMARKS
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
                            3,
                            (0, 255, 0),
                            -1
                        )

                # =================================================
                # HIGHLIGHT IMPORTANT JOINTS
                # =================================================

                important_points = [
                    shoulder_point,
                    elbow_point,
                    wrist_point,
                    hip_point,
                    knee_point,
                    ankle_point
                ]

                for point in important_points:

                    cv2.circle(
                        frame,
                        point,
                        8,
                        (0, 0, 255),
                        -1
                    )

                # =================================================
                # ARM LINES
                # =================================================

                cv2.line(
                    frame,
                    shoulder_point,
                    elbow_point,
                    (255, 255, 0),
                    3
                )

                cv2.line(
                    frame,
                    elbow_point,
                    wrist_point,
                    (255, 255, 0),
                    3
                )

                # =================================================
                # BODY LINES
                # =================================================

                cv2.line(
                    frame,
                    shoulder_point,
                    hip_point,
                    (255, 255, 0),
                    3
                )

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
                # UI HEADER
                # =================================================

                cv2.putText(
                    frame,
                    "FITNOVA - PUSH-UP",
                    (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2
                )

                # =================================================
                # SIDE
                # =================================================

                cv2.putText(
                    frame,
                    f"Detected side: {detected_side}",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

                # =================================================
                # ELBOW ANGLE
                # =================================================

                cv2.putText(
                    frame,
                    f"Elbow: {int(elbow_angle)} deg",
                    (20, 105),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

                # =================================================
                # STATE
                # =================================================

                cv2.putText(
                    frame,
                    f"State: {state}",
                    (20, 140),
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
                    f"Reps: {reps}",
                    (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2
                )

                # =================================================
                # FORM
                # =================================================

                cv2.putText(
                    frame,
                    f"Form: {form_score}/100",
                    (20, 220),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2
                )

                # =================================================
                # ALIGNMENT
                # =================================================

                cv2.putText(
                    frame,
                    f"Alignment: {alignment_status}",
                    (20, 255),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

                # =================================================
                # FEEDBACK
                # =================================================

                cv2.putText(
                    frame,
                    f"Feedback: {feedback}",
                    (20, 290),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2
                )

                # =================================================
                # INSTRUCTION
                # =================================================

                if state == "UP":

                    instruction = "Start push-up"

                elif state == "GOING_DOWN":

                    instruction = "Keep going down"

                elif state == "DOWN":

                    instruction = (
                        "Good depth - push up"
                    )

                else:

                    instruction = "Push up"

                cv2.putText(
                    frame,
                    instruction,
                    (20, height - 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2
                )

            # =================================================
            # SIDE NOT LOCKED
            # =================================================

            else:

                cv2.putText(
                    frame,
                    "Detecting body side...",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "Move your full body into view",
                    (20, 85),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

        # ====================================================
        # NO PERSON DETECTED
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
        # DISPLAY
        # ====================================================

        cv2.imshow(
            "FitNova - Push-up AI Coach",
            frame
        )

        # ====================================================
        # KEYBOARD
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
    # FINAL SUMMARY
    # ========================================================

    summary = workout_session.get_summary()

    # ========================================================
    # SAVE TO WORKOUT HISTORY
    # ========================================================

    saved = workout_history.add_workout(
        summary
    )

    # ========================================================
    # DISPLAY FINAL SUMMARY
    # ========================================================

    print()
    print("==========================================")
    print("       FITNOVA PUSH-UP SUMMARY")
    print("==========================================")
    print()

    print(
        f"Exercise       : "
        f"{summary['exercise']}"
    )

    print(
        f"Total Reps     : "
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
            "WARNING: Workout could not be saved."
        )

    print()

    print("==========================================")
    print("          SESSION COMPLETE")
    print("==========================================")
    print()

    input(
        "Press Enter to return to FitNova..."
    )


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    run_pushup_detection()