from models.database import Database
import os
import pickle

def generate_admin_data():
    admin_file = os.path.join(os.path.dirname(__file__), "../data/admins.data")

    # Define admin users
    admin_users = [
        {"username": "admin1", "password": "Admin123"},
        {"username": "admin2", "password": "Secure456"},
    ]

    # Save admin users to the file
    with open(admin_file, "wb") as file:
        pickle.dump(admin_users, file)

    print("Admin data has been successfully generated!")

if __name__ == "__main__":
    generate_admin_data()
