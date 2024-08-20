#autologin with delay and capture
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import os

# Path to save cookies
cookies_file = 'cookies.pkl'

# Function to save cookies
def save_cookies(driver):
    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

# Function to load cookies
def load_cookies(driver):
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

# Function to log in to TradingView
def login_to_tradingview(driver, email, password):
    driver.get("https://www.tradingview.com/accounts/signin/")
    
    try:
        if not os.path.exists(cookies_file):
            # Perform login only if cookies file doesn't exist
            email_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="id_username"]'))
            )
            email_input.send_keys(email)

            password_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="id_password"]'))
            )
            password_input.send_keys(password)

            login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[2]/div/div/div/form/button/span/span'))
            )
            login_button.click()

            # Allow time for the login to complete
            time.sleep(10)
            
            # Save cookies after successful login
            save_cookies(driver)
        else:
            # Load cookies if the file exists
            driver.get("https://www.tradingview.com/")
            load_cookies(driver)
            driver.refresh()

    except Exception as e:
        print("An error occurred during login:", e)

# Setup Chrome options
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Function to log in to TradingView
def login_to_tradingview(driver, email, password):
    driver.get("https://www.tradingview.com/accounts/signin/")

    try:
        # Fill in the email field
        email_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="id_username"]'))
        )
        email_input.send_keys(email)
        time.sleep(10)
        # Fill in the password field
        password_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="id_password"]'))
        )
        password_input.send_keys(password)
        time.sleep(10)
        # Click the login button
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[2]/div/div/div/form/button/span/span'))
        )
        login_button.click()

        # Allow time for the login to complete
        time.sleep(10)

    except Exception as e:
        print("An error occurred during login:", e)

# Function to capture and return OHLC values along with date and time
def capture_ohlc(driver):
    try:
        open_value = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]'))
        ).text

        high_value = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[3]/div[2]'))
        ).text

        low_value = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[4]/div[2]'))
        ).text

        close_value = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[5]/div[2]'))
        ).text

        month = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div'))
        ).text

        day = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div'))
        ).text

        year = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[3]/div'))
        ).text

        hour = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[4]/div'))
        ).text

        minute = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[5]/div'))
        ).text

        return open_value, high_value, low_value, close_value, f"{year}-{month}-{day} {hour}:{minute}"

    except Exception as e:
        print("An error occurred while capturing OHLC:", e)
        return None, None, None, None, None

# Function to write OHLC data to a CSV file
def write_ohlc_to_csv(csv_file, ohlc_data):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(ohlc_data)

# Function to move the chart left and capture OHLC data
def move_chart_and_capture_ohlc(driver, csv_file, movements=10):
    actions = ActionChains(driver)

    for _ in range(movements):
        # Capture OHLC values and time data
        ohlc_data = capture_ohlc(driver)

        # Write the OHLC values and time data to the CSV file
        if ohlc_data[0] is not None:
            write_ohlc_to_csv(csv_file, ohlc_data)

        # Move the chart to the left by pressing the left arrow key
        actions.send_keys('\ue012').perform()  # \ue012 is the key code for the left arrow key

        # Allow time for the chart to update
        time.sleep(1)

def get_number_of_movements(driver):
    movements_text = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[4]/div[2]/div/div/div'))
    ).text
    
    # Remove commas and convert to integer
    movements_text = movements_text.replace(',', '')
    return int(float(movements_text))


def get_dynamic_filename(driver):
    name = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button'))
    ).text

    timeframe = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/button'))
    ).text

    return f"{name}_{timeframe}.csv"



# Main function to run the process
def main(email, password):
    driver = setup_driver()

    # Log in to TradingView
    login_to_tradingview(driver, email, password)

    # Open TradingView chart URL
    driver.get("https://www.tradingview.com/chart/Ow6LCR4w/")  # Update the URL to the specific chart if necessary

    # Allow the page to load completely
    time.sleep(60)

    # Get dynamic filename
    csv_file = get_dynamic_filename(driver)

    # Write CSV header
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Open', 'High', 'Low', 'Close', 'Datetime'])

    # Get the number of movements
    movements = get_number_of_movements(driver)

    # Move the chart and capture OHLC data
    move_chart_and_capture_ohlc(driver, csv_file, movements=movements)

    # Close the browser
    driver.quit()

    print(f"OHLC and time data has been saved to {csv_file}.")



# Execute the main function
if __name__ == "__main__":
    # Replace with your TradingView credentials
    email = "gauranshhitachi@gmail.com"
    password = "Trad3!ndi@Gogo"
    main(email, password)
