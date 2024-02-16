import hashlib
import random
import string
import requests
import time

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(random.randint(8, 20)))

def generate_random_email():
    email = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10)))
    domain = random.choice(["@gmail.com", "@yahoo.com", "@outlook.com"])
    return email + domain

def create_credentials_file():
    with open("correct_credentials.txt", "w") as file:
        file.write("Email:Password\n")

def save_credentials(email, password):
    with open("correct_password.txt", "a") as file:
        file.write(f"{email}:{password}\n")

def check_website_access(website):
    try:
        response = requests.get(website)
        if response.status_code == 200:
            return True
        else:
            print("Cannot access the website. Please try again.")
            return False
    except requests.exceptions.RequestException:
        print("Cannot access the website. Please try again.")
        return False

def brute_force(website):
    found_password = None
    tried_emails = set()
    password = generate_password()
    attempts = 0

    while not found_password:
        email = generate_random_email()

        if email in tried_emails:
            continue

        tried_emails.add(email)

        combination = f"{email}:{password}"

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"{email}: {password}", end=" - ")

        if hashed_password == "YOUR_DESIRED_HASH":
            found_password = password
            print("Correct")
            break
        else:
            print("Incorrect")
            attempts += 1

            if attempts >= 4:
                print("Refreshing the page...")
                time.sleep(3)  # Simulating the page refresh delay
                attempts = 0

    if found_password:
        save_credentials(email, found_password)
        print("Correct credentials found and logged to correct_password.txt")

# Create the "correct_credentials.txt" file when the script starts
create_credentials_file()

# Main loop
while True:
    website = input("Enter the website you want to target: ")

    if not check_website_access(website):
        continue

    brute_force(website)