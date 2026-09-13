from collections import deque


class AngleSmoother:
    """
    Smooths noisy angle measurements by averaging
    the most recent readings.
    """

    def __init__(self, window_size=5):

        self.window_size = window_size

        self.angles = deque(
            maxlen=window_size
        )


    def update(self, angle):

        # Add new angle
        self.angles.append(angle)

        # Calculate average
        smoothed_angle = sum(
            self.angles
        ) / len(self.angles)

        return smoothed_angle


    def reset(self):

        self.angles.clear()