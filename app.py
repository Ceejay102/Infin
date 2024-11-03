from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# Initialize the Chrome driver
#driver = webdriver.Chrome()  # or use `webdriver.Firefox()` depending on your browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# URL of the news site
url = "https://news.google.com"  # Replace with the actual URL if it's different

# List of main tabs and their sub-tabs
tabs = {
    "Business": ["Latest", "Economy", "Markets", "Job", "Personal finance", "Entrepreneurship"],
    "Technology": ["Latest", "Mobile", "Gadget", "Internet", "Virtual reality", "Artificial intelligence", "Computing"],
    "Entertainment": ["Latest", "Movies", "Music", "TV", "Books", "Arts & design", "Celebrities"]
}

# Open the main page
driver.get(url)
wait = WebDriverWait(driver, 10)

# Prepare the CSV file
with open("news_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Tab", "Sub-tab", "Headline", "Link"])

    # Iterate over each main tab
    for tab_name in tabs:
        try:
            # Click on the main tab
            main_tab = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, tab_name))
            )
            main_tab.click()
            time.sleep(2)  # Wait for the tab page to load
            
            # Iterate over each sub-tab within the main tab
            for sub_tab_name in tabs[tab_name]:
                try:
                    # Find and click the sub-tab button
                    sub_tab_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[@aria-label='{sub_tab_name}']"))
                    )
                    sub_tab_button.click()
                    time.sleep(2)  # Wait for the sub-tab page to load
                    
                    # Scrape headlines and links
                    headlines = driver.find_elements(By.CSS_SELECTOR, "a.WwrzSb")
                    for headline in headlines:
                        title = headline.text
                        link = headline.get_attribute("href")
                        csvwriter.writerow([tab_name, sub_tab_name, title, link])
                
                except Exception as e:
                    print(f"Error with sub-tab '{sub_tab_name}' in '{tab_name}': {e}")
        
        except Exception as e:
            print(f"Error with main tab '{tab_name}': {e}")

# Close the driver
driver.quit()
print("Scraping completed. Data saved to news_data.csv.")
