import pandas as pd
import os

USER_CSV = "users.csv"

# Load users from CSV file
def load_users():
    if os.path.exists(USER_CSV):
        return pd.read_csv(USER_CSV)
    return pd.DataFrame(columns=["first_name", "last_name", "mobile", "password"])

# Save a new user to the CSV
def save_user(first_name, last_name, mobile, password):
    if not password:
        print("ERROR: Password is empty!")
        return

    new_user = pd.DataFrame([[first_name, last_name, mobile, password]],
                            columns=["first_name", "last_name", "mobile", "password"])
    all_users = load_users()

    # Debugging: Show what is being saved
    print(f"Saving new user: {new_user}")

    all_users = pd.concat([all_users, new_user], ignore_index=True)
    all_users.to_csv(USER_CSV, index=False)

    # Debugging: Ensure data is saved correctly
    print(f"Saved users to CSV: {all_users}")

# Check if user already exists
def user_exists(mobile):
    users = load_users()
    return mobile in users["mobile"].values

# Validate user credentials
def validate_user(mobile, password):
    users = load_users()
    user_row = users[users["mobile"] == mobile]

    # Debugging: Show the data being checked
    print(f"Users in database: {users}")
    print(f"Checking credentials for mobile: {mobile}, password: {password}")

    if not user_row.empty:
        stored_password = user_row.iloc[0]["password"]
        print(f"Stored password: {stored_password}")  # Debugging: Check stored password
        if stored_password == password:
            print(f"User {mobile} validated successfully.")
            return user_row.iloc[0]  # Return the user data as a row
    print(f"Invalid credentials for {mobile}.")
    return False
