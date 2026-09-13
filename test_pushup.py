from pushup_analyzer import PushUpAnalyzer


analyzer = PushUpAnalyzer()


test_angles = [
    170,
    160,
    140,
    120,
    100,
    90,
    100,
    120,
    145,
    160,
    170
]


print()
print("==========================================")
print("       FITNOVA PUSH-UP TEST")
print("==========================================")
print()


for angle in test_angles:

    reps, state = analyzer.update(
        angle
    )

    score = analyzer.get_form_score(
        angle
    )

    feedback = analyzer.get_feedback(
        angle
    )

    print(
        f"Angle: {angle:3d}° | "
        f"State: {state:10s} | "
        f"Reps: {reps} | "
        f"Score: {score} | "
        f"{feedback}"
    )


print()
print("==========================================")
print(
    f"Final repetitions: {analyzer.reps}"
)
print("==========================================")