class ExerciseSelector:
    """
    Handles exercise selection for FitNova.
    """

    def __init__(self):

        self.exercises = {
            "1": "Squat",
            "2": "Push-up",
            "3": "Bicep Curl"
        }

    def display_exercises(self):

        print()
        print("==========================================")
        print("          FITNOVA EXERCISE MENU")
        print("==========================================")
        print()

        for number, exercise in self.exercises.items():

            print(f"{number}. {exercise}")

        print()

    def get_exercise(self):

        while True:

            self.display_exercises()

            choice = input(
                "Select an exercise (1-3): "
            ).strip()

            if choice in self.exercises:

                selected_exercise = self.exercises[choice]

                print()
                print(
                    f"Selected exercise: "
                    f"{selected_exercise}"
                )
                print()

                return selected_exercise

            print()
            print("Invalid choice.")
            print("Please select 1, 2, or 3.")
            print()