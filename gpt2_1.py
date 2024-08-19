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

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Enable GPU acceleration
chrome_options.add_argument("--window-size=1920,1080")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to capture and return OHLC values
def capture_ohlc():
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

    return open_value, high_value, low_value, close_value

# CSV file to store the OHLC data
csv_file = "ohlc_data.csv"

# Open the CSV file in write mode and write the header
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Open', 'High', 'Low', 'Close'])

try:
    # Open TradingView chart URL
    driver.get("https://www.tradingview.com/chart/")  # Update the URL to the specific chart if necessary

    # Allow the page to load completely
    time.sleep(5)

    # Initialize ActionChains for keyboard interaction
    actions = ActionChains(driver)

    for _ in range(10):  # Adjust the range for the number of movements you want
        # Capture OHLC values
        open_value, high_value, low_value, close_value = capture_ohlc()

        # Write the OHLC values to the CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([open_value, high_value, low_value, close_value])

        # Move the chart to the left by pressing the left arrow key
        actions.send_keys('\ue012').perform()  # \ue012 is the key code for the left arrow key

        # Allow time for the chart to update
        time.sleep(1)

finally:
    # Close the browser
    driver.quit()

print(f"OHLC data has been saved to {csv_file}.")
