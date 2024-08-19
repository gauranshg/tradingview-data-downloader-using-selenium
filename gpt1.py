from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize WebDriver (assuming you're using Chrome)
driver = webdriver.Chrome()

# TradingView chart URL
url = "https://www.tradingview.com/chart/"
driver.get(url)

# Wait until the chart loads (adjust the waiting time as needed)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "chart-container")))

# Give some time for all elements to load
time.sleep(5)

# Example function to extract OHLC data from the TradingView chart
def extract_ohlc_data():
    ohlc_data = []

    # Extracting Open, High, Low, and Close values using the provided XPath for "Open" and similar for others
    candles = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "valueValue-l31H9iuA", " " ))]')

    for candle in candles:
        try:
            # Use XPath to extract Open, High, Low, and Close values
            open_price = candle.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "valueValue-l31H9iuA", " " ))]').text
            high_price = candle.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "valueValue-l31H9iuA", " " ))]').text
            low_price = candle.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "valueValue-l31H9iuA", " " ))]').text
            close_price = candle.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "valueValue-l31H9iuA", " " ))]').text
            ohlc_data.append([open_price, high_price, low_price, close_price])
        except Exception as e:
            print(f"Error extracting candle data: {e}")
            continue
    
    return ohlc_data

# Extract OHLC data
ohlc_data = extract_ohlc_data()

# Save to CSV
df = pd.DataFrame(ohlc_data, columns=["Open", "High", "Low", "Close"])
df.to_csv("ohlc_data.csv", index=False)
input("input")
# Close the WebDriver
driver.quit()

print("OHLC data saved to ohlc_data.csv")
