from utils import calculate_angle


# Example points
hip = (100, 100)
knee = (100, 200)
ankle = (200, 200)

angle = calculate_angle(hip, knee, ankle)

print("Calculated angle:", angle)