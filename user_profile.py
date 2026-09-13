import json
from pathlib import Path


class UserProfile:
    """
    Stores and manages the FitNova user's fitness profile.

    The profile is used by the AI Coach to create:
    - Personalized workout plans
    - Sets and repetitions
    - Daily recommendations
    - Adaptive workout routines
    - Nutrition and recipe suggestions
    """

    def __init__(self):

        # ========================================================
        # PROFILE FILE
        # ========================================================

        self.file_path = (
            Path(__file__).resolve().parent
            / "user_profile.json"
        )

        # ========================================================
        # DEFAULT PROFILE
        # ========================================================

        self.profile = self.get_default_profile()

        # ========================================================
        # LOAD EXISTING PROFILE
        # ========================================================

        self.load_profile()

    # ============================================================
    # DEFAULT PROFILE
    # ============================================================

    def get_default_profile(self):
        """
        Return an empty/default user profile.
        """

        return {
            "name": "",
            "age": 0,
            "gender": "",
            "height": 0,
            "weight": 0,

            "fitness_goal": "",
            "fitness_level": "",

            "workout_days": 0,
            "workout_duration": 30,

            "equipment": [],

            "diet": "",
            "allergies": [],

            "preferred_exercises": [],

            "created_at": "",
            "updated_at": ""
        }

    # ============================================================
    # LOAD PROFILE
    # ============================================================

    def load_profile(self):
        """
        Load the user profile from JSON.
        """

        if not self.file_path.exists():

            return False

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, dict):

                self.profile.update(data)

                return True

        except (
            json.JSONDecodeError,
            OSError
        ):

            print(
                "Warning: Could not load user profile."
            )

        return False

    # ============================================================
    # SAVE PROFILE
    # ============================================================

    def save_profile(self):
        """
        Save the current profile to JSON.
        """

        try:

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.profile,
                    file,
                    indent=4
                )

            return True

        except OSError as error:

            print(
                f"Could not save user profile: {error}"
            )

            return False

    # ============================================================
    # SET PROFILE
    # ============================================================

    def set_profile(
        self,
        name,
        age,
        gender,
        height,
        weight,
        fitness_goal,
        fitness_level,
        workout_days,
        workout_duration,
        equipment,
        diet,
        allergies,
        preferred_exercises
    ):
        """
        Create or update the complete user profile.
        """

        from datetime import datetime

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        # --------------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------------

        self.profile["name"] = name
        self.profile["age"] = age
        self.profile["gender"] = gender

        # --------------------------------------------------------
        # BODY INFORMATION
        # --------------------------------------------------------

        self.profile["height"] = height
        self.profile["weight"] = weight

        # --------------------------------------------------------
        # FITNESS INFORMATION
        # --------------------------------------------------------

        self.profile["fitness_goal"] = fitness_goal
        self.profile["fitness_level"] = fitness_level

        self.profile["workout_days"] = workout_days
        self.profile["workout_duration"] = workout_duration

        # --------------------------------------------------------
        # EQUIPMENT
        # --------------------------------------------------------

        self.profile["equipment"] = equipment

        # --------------------------------------------------------
        # NUTRITION
        # --------------------------------------------------------

        self.profile["diet"] = diet
        self.profile["allergies"] = allergies

        # --------------------------------------------------------
        # EXERCISE PREFERENCES
        # --------------------------------------------------------

        self.profile["preferred_exercises"] = (
            preferred_exercises
        )

        # --------------------------------------------------------
        # TIMESTAMPS
        # --------------------------------------------------------

        if not self.profile["created_at"]:

            self.profile["created_at"] = now

        self.profile["updated_at"] = now

        # --------------------------------------------------------
        # SAVE
        # --------------------------------------------------------

        return self.save_profile()

    # ============================================================
    # GET PROFILE
    # ============================================================

    def get_profile(self):
        """
        Return the complete profile.
        """

        return self.profile.copy()

    # ============================================================
    # GET VALUE
    # ============================================================

    def get(self, key, default=None):
        """
        Get a specific profile value.
        """

        return self.profile.get(
            key,
            default
        )

    # ============================================================
    # UPDATE SINGLE VALUE
    # ============================================================

    def update(self, key, value):
        """
        Update one profile field.
        """

        from datetime import datetime

        if key not in self.profile:

            return False

        self.profile[key] = value

        self.profile["updated_at"] = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        return self.save_profile()

    # ============================================================
    # CHECK PROFILE
    # ============================================================

    def is_complete(self):
        """
        Check whether the important profile information
        has been provided.
        """

        required_fields = [
            "name",
            "age",
            "gender",
            "height",
            "weight",
            "fitness_goal",
            "fitness_level",
            "workout_days",
            "workout_duration",
            "diet"
        ]

        for field in required_fields:

            value = self.profile.get(
                field
            )

            if value in (
                None,
                "",
                0
            ):

                return False

        return True

    # ============================================================
    # DISPLAY PROFILE
    # ============================================================

    def display_profile(self):
        """
        Display the user's profile.
        """

        print()
        print("=" * 55)
        print("              FITNOVA USER PROFILE")
        print("=" * 55)
        print()

        print(
            f"Name             : "
            f"{self.profile['name']}"
        )

        print(
            f"Age              : "
            f"{self.profile['age']}"
        )

        print(
            f"Gender           : "
            f"{self.profile['gender']}"
        )

        print(
            f"Height           : "
            f"{self.profile['height']} cm"
        )

        print(
            f"Weight           : "
            f"{self.profile['weight']} kg"
        )

        print(
            f"Fitness Goal     : "
            f"{self.profile['fitness_goal']}"
        )

        print(
            f"Fitness Level    : "
            f"{self.profile['fitness_level']}"
        )

        print(
            f"Workout Days     : "
            f"{self.profile['workout_days']}"
        )

        print(
            f"Workout Duration : "
            f"{self.profile['workout_duration']} minutes"
        )

        print(
            f"Equipment        : "
            f"{', '.join(self.profile['equipment'])}"
        )

        print(
            f"Diet             : "
            f"{self.profile['diet']}"
        )

        print(
            f"Allergies        : "
            f"{', '.join(self.profile['allergies'])}"
        )

        print(
            f"Exercises        : "
            f"{', '.join(self.profile['preferred_exercises'])}"
        )

        print()

        print("=" * 55)
        print()

    # ============================================================
    # RESET PROFILE
    # ============================================================

    def reset_profile(self):
        """
        Reset the profile to default values.
        """

        self.profile = (
            self.get_default_profile()
        )

        return self.save_profile()