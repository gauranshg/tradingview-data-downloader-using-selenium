#autologin with delay and capture 
#options downloader
#gpt_2_2_7.py
#debug
#log.csv
#mouse move
#rerun 

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
import pandas as pd
import pyautogui
import pygetwindow as gw
import pyautogui
import time
from selenium.common.exceptions import NoSuchElementException

debug_v = False
failed =[]
force_rerun = True
max_run = 1

def delete_element_if_exists(xpath, driver):
    try:
        element = driver.find_element("xpath", xpath)
        # Execute JavaScript to remove the element
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
        print(f"Deleted element: {xpath}")
    except NoSuchElementException:
        print(f"Element not found: {xpath}")

def debug(driver):
    delete_element_if_exists("/html/body/div[6]/div[3]/div/div[2]",driver)
    delete_element_if_exists("/html/body/div[6]/div[3]/div/div",driver)
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x, current_y + 5)
    time.sleep(1)
    pyautogui.moveTo(current_x, current_y)

def maximize_and_focus_window(partial_title):
    # Find windows that contain the partial title
    matching_windows = [w for w in gw.getAllWindows() if partial_title.lower() in w.title.lower()]
    
    if not matching_windows:
        print(f"No window found with title containing '{partial_title}'.")
        return

    # Use the first matching window
    window = matching_windows[0]

    # Maximize the window if it's not already maximized
    if not window.isMaximized:
        window.maximize()

    # Bring the window to the front
    window.activate()

    # Focus on the window by clicking at its center
    window_center = window.center
    pyautogui.click(window_center.x, window_center.y)

    print(f"Maximized and focused on window with title '{window.title}'.")






def remove_duplicates(input_csv, output_csv):
    """
    Opens a CSV file, removes duplicate rows based on the 'Datetime' column,
    and saves the cleaned data to a new CSV file.
    
    Args:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file where cleaned data will be saved.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Remove duplicates based on the 'Datetime' column
    df_cleaned = df.drop_duplicates(subset='Datetime')
    
    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_csv, index=False)

    return len(df_cleaned)

# Example usage
def generate_scrip_list(base, date, strike_range, interval, tf_list):
    scrips = []
    
    for strike in range(strike_range[0], strike_range[1] + interval, interval):
        for tf in tf_list:
            scrip = f"{base}{date}C{strike:05d}"
            scrips.append({"scrip": scrip, "TF": tf})
        for tf in tf_list:
            scrip = f"{base}{date}P{strike:05d}"
            scrips.append({"scrip": scrip, "TF": tf})
    
    if debug_v:
        return scrips[0:2]


    return scrips





# Path to save cookies
cookies_file = 'cookies.pkl'

list_of_values = [{"scrip":"NIFTY", "TF":"5"},{"scrip":"BANKNIFTY", "TF":"60"}]

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
            print_sleep(10)
            
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
    chrome_options.add_argument("--start-maximized")
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

        # Fill in the password field
        password_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="id_password"]'))
        )
        password_input.send_keys(password)

        # Click the login button
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[2]/div/div/div/form/button/span/span'))
        )
        login_button.click()

        # Allow time for the login to complete
        print_sleep(10)

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
    #print("Writing")
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(ohlc_data)

# Function to move the chart left and capture OHLC data
def move_chart_and_capture_ohlc(driver, csv_file, movements=10):
    if debug_v:
        movements = 10

    actions = ActionChains(driver)
    latest_ohlc_data = capture_ohlc(driver)
    print(latest_ohlc_data)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        threshold = 0
        for i in range(movements):
            if i > 10:
                threshold = 10
            print("t: " + str(threshold) +" i: " + str(i))
            # Capture OHLC values and time data
            ohlc_data = capture_ohlc(driver)
            print(ohlc_data)
            while ohlc_data == latest_ohlc_data and threshold > 0:
                print("debugging")
                debug(driver)
                ohlc_data = capture_ohlc(driver)
                threshold = threshold - 1
                if threshold <= 0:
                    return

            # Write the OHLC values and time data to the CSV file
            if ohlc_data[0] is not None:
                writer.writerow(ohlc_data)

            # Move the chart to the left by pressing the left arrow key
            actions.send_keys('\ue012').perform()  # \ue012 is the key code for the left arrow key

            # Allow time for the chart to update
            time.sleep(0.01)

def get_number_of_movements(driver):
    print("finding total number of bars")
    movements_text = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[3]/div[2]/div/div/div'))
    ).text
    
    # Remove commas and convert to integer
    movements_text = movements_text.replace(',', '')
    print(movements_text)
    return int(float(movements_text))



def get_dynamic_filename(driver):
    print("Fetching name")
    name = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/button'))
    ).text

    timeframe = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/button'))
    ).text
    print(f"{name}_{timeframe}.csv")
    return f"{name}_{timeframe}.csv"

def print_sleep(n):
    for i in range(n):
        print(i)
        time.sleep(1)

def download_scrip(driver,link):
    driver.get(link)  # Update the URL to the specific chart if necessary
    #maximize_and_focus_window("Unnamed")
    # Allow the page to load completely
    print_sleep(5)
    current_x, current_y = pyautogui.position()

# Move the mouse 5 pixels down (vertically)


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
    rows = remove_duplicates(csv_file, 'cleaned_'+csv_file)
    return csv_file, rows, movements


# Main function to run the process
def main(email, password,list_of_values):
    driver = setup_driver()
    
    for item in list_of_values:
        print(item)

    # Log in to TradingView
    #login_to_tradingview(driver, email, password)
    failed = []
    # Open TradingView chart URL
    for item in list_of_values:
        scrip = item["scrip"]
        tf = item["TF"]
        url = f"https://www.tradingview.com/chart/Ow6LCR4w/?symbol={scrip}&interval={tf}"
        csv_file, rows, movemments = download_scrip(driver, url)
        if not os.path.isfile("log.csv"):
            with open("log.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Scrip","TF","Cleaned" "rows","Totalrows","Debug","FileName"])

        with open("log.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([scrip,tf,rows,movemments,str(debug_v),csv_file])
        
        if rows/movemments < 0.9:
            failed.append({"scrip": scrip, "TF": tf})

        print(f"OHLC and time data has been saved to {csv_file}.")

    # Close the browser
    driver.quit()

    if len(failed) > 0:
        list_of_values = failed
        for items in list_of_values:
            print(items)
        if not force_rerun:
            rerun = input("Do you want to run the code for failed cases? (Y/n)")
        else:
            rerun = "Y"
            global max_run
            max_run = max_run-1
            if max_run < 0:
                return

        if rerun == "Y":
            main("","",list_of_values)
        else:
            print("Exiting")


# Execute the main function
if __name__ == "__main__":
    # Replace with your TradingView credentials
    base = "BANKNIFTY"
    date = "240821"
    strike_range = (48500, 54000)  # Range of strikes
    interval = 100  # Interval between strikes
    tf_list = ["15"]  # List of timeframes

    # Generate list
    #list_of_values = generate_scrip_list(base, date, strike_range, interval, tf_list)
    list_of_values = [{"scrip":"NIFTY", "TF":"15"},{"scrip":"BANKNIFTY", "TF":"15"},{"scrip":"FINIFTY", "TF":"15"}]
    for item in list_of_values:
        print(item)
    main("", "",list_of_values)
