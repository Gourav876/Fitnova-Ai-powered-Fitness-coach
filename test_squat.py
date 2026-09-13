from squat_analyzer import SquatAnalyzer


analyzer = SquatAnalyzer()


# Simulated knee angles
test_angles = [
    170,   # Standing
    150,   # Going down
    130,   # Going down
    105,   # Squat
    120,   # Going up
    145,   # Going up
    170    # Standing
]


for angle in test_angles:

    reps, state = analyzer.update(angle)

    print(
        f"Angle: {angle}° | "
        f"State: {state} | "
        f"Reps: {reps}"
    )