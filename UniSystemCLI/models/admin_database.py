import os
import pickle

class AdminDatabase:
    def __init__(self):
        # Path to the admin data file
        self.filepath = os.path.join(os.path.dirname(__file__), "../data/admins.data")

    def load_admins(self):
        """Load all admin users from the data file."""
        if not os.path.exists(self.filepath):
            return []  # Return an empty list if the file doesn't exist
        try:
            with open(self.filepath, "rb") as file:
                return pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            # Handle empty or corrupted file
            return []

    def save_admins(self, admins):
        """Save the list of admin users to the data file."""
        with open(self.filepath, "wb") as file:
            pickle.dump(admins, file)
