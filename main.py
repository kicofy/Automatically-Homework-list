#######################################################################################
username = "...@..."  # Your username for login
password = "......."  # Your password for login
driver_path = ""     # Leave empty to use msedgedriver.exe in current folder
                     # Or input the path to your browser driver, like "C:/WebDriver/chromedriver.exe"
#######################################################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


# Function to parse homework data from the HTML source of the iframe
def parse_homework(html_source):
    # BeautifulSoup is used to parse HTML, making it easy to extract specific data
    soup = BeautifulSoup(html_source, 'html.parser')

    # List to store parsed homework data
    homework_data = []

    # Find all date blocks and homework blocks
    date_boxes = soup.find_all('div', class_='pwr_date_hr')
    homework_sections = soup.find_all('section', class_='pwr_card_content')

    current_date = None
    current_day_of_week = None

    # Iterate through all elements to match date and homework blocks
    for element in soup.find_all(['div', 'section']):
        if element.name == 'div' and 'pwr_date_hr' in element.get('class', []):
            # Update current date and day of the week if it's a date block
            current_day_of_week = element.find('span', class_='pwr_day').text.strip()
            current_date = element.find('span', class_='pwr_date').text.strip()
        
        elif element.name == 'section' and 'pwr_card_content' in element.get('class', []):
            # Extract homework details based on the current date and day of the week
            subject = element.find('h3', class_='pwr_card-heading alt').text.strip()
            homework_content = element.find('p').text.strip() if element.find('p') else "No content available"

            # Create a dictionary to represent one homework item
            homework_item = {
                'date': current_date,
                'day_of_week': current_day_of_week,
                'subject': subject,
                'content': homework_content
            }

            # Add the dictionary to the homework data list
            homework_data.append(homework_item)

    return homework_data


# Configure Edge browser options
edge_options = Options()
#edge_options.add_argument("--headless")  # Enable headless mode to hide the browser window
edge_options.add_argument("--disable-gpu")  # Disable GPU acceleration (useful for headless mode)
edge_options.add_argument("--start-maximized")  # Browser will start maximized (does not affect headless mode)

# Explanation: Edge options configure how the browser behaves when launched. The `--headless` argument
# makes the browser run in the background, useful for automation that doesn't need a visible UI.

# Set the path to EdgeDriver
driver_path = 'msedgedriver.exe'  # Replace with the actual path to your EdgeDriver
service = Service(driver_path)

# Launch Edge browser in headless mode
driver = webdriver.Edge(service=service, options=edge_options)

try:
    print("Step 1: Opening the login page")
    driver.get("https://familyportal.renweb.com/")

    print("Step 2: Waiting for and locating the District Code input field")
    # WebDriverWait waits dynamically for elements to appear instead of fixed delays.
    district_code_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "rw-district-code"))
    )
    district_code_field.send_keys("tcs-nj")  # Enter the district code

    print("Step 3: Waiting for and locating the Username input field")
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "rw-username"))
    )
    username_field.send_keys(username)  # Enter your username

    print("Step 4: Waiting for and locating the Password input field")
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "rw-password"))
    )
    password_field.send_keys(password)  # Enter your password

    # Explanation: `WebDriverWait` allows waiting for elements dynamically, avoiding hardcoded delays.
    # It waits until a specific condition (like element presence or visibility) is met.

    print("Step 5: Submitting the login form")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "next"))
    )
    login_button.click()

    print("Step 6: Waiting for the page to load and navigating to the homework page")
    time.sleep(5)  # A static wait; you can replace it with a more precise wait condition
    driver.get("https://familyportal.renweb.com/en-us/student/homework")

    print("Step 7: Waiting for the homework page to load")
    time.sleep(5)

    # Explanation: Static waits (`time.sleep`) are used when the exact condition cannot be dynamically
    # checked. However, they are less efficient and should be replaced with `WebDriverWait` if possible.

    print("Step 8: Switching to iframe and extracting the page source")
    iframe_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe_element)

    # Explanation: Many web pages use `<iframe>` to embed content. To interact with such content, you must
    # switch to the iframe using `driver.switch_to.frame()`.

    # Extract HTML source from the iframe
    iframe_source = driver.page_source
    
    print("Step 9: Parsing homework data from the page source")
    homework_list = parse_homework(iframe_source)
    
    # Display parsed homework data
    for item in homework_list:
        print(f"Date: {item['date']} - Day: {item['day_of_week']} - Subject: {item['subject']} - Homework: {item['content']}")
    
    # Switch back to the main page content
    driver.switch_to.default_content()

finally:
    print("Step 10: Closing the browser")
    driver.quit()

    # Explanation: The `try-finally` block ensures the browser is closed properly, even if an error occurs
    # during execution. This avoids leaving browser processes running in the background.
