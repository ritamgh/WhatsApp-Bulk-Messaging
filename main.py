import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def config():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/home/atom/.config/google-chrome")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.binary_location = "/opt/google/chrome/google-chrome"
    chrome_options.add_argument("--verbose")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

driver = config()

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')

# Load the dataset
df = pd.read_csv('./Dataset/fake.csv')

message = """🎉 *Congratulations!* 🎉 

You have been selected for the interview round of NextGenAI's Generative AI domain's recruitment! 🥳 We’re excited to learn more about you.

📝 Please fill out the Google form below to select your preferred interview time slot. The interviews will be held from *Sunday to Saturday* 🗓️ between *6 PM and 12 PM*

https://docs.google.com/forms/d/e/1FAIpQLSd3y2Wqf9GkvmTzILBPNj9pU1FzrWYLJdEyf4hhFl9xcFSGMg/viewform?usp=sharing

📍Link to Whatsapp group
https://chat.whatsapp.com/FmHE8iNh3G5EC2mW70uFcM

Looking forward to meeting you! 🌟"""
message_encoded = message.replace("\n", "%0A")

# Loop through each contact in the dataset
for index, row in df.iterrows():
    try:
        name = row['Name']
        phone_number = row['Phone number']

        # Add the country code (e.g., for India, add +91)
        phone_number_with_code = f"+91{phone_number}"

        # Navigate to the WhatsApp chat for the phone number
        url = f"https://web.whatsapp.com/send?phone={phone_number_with_code}&text={message_encoded}"
        driver.get(url)

        # Wait for the chat to load and the send button to become clickable
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
        )

        # Find and click the send button
        send_button = driver.find_element(By.XPATH, '//button[@aria-label="Send"]')
        send_button.click()

        # Wait for a few seconds before sending the next message
        time.sleep(10)

    except Exception as e:
        print(f"Error sending message to {phone_number}: {str(e)}")

# Close the browser after sending all messages
driver.quit()
