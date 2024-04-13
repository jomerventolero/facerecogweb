from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Initialize the WebDriver
driver = webdriver.Chrome()  # You can use any other WebDriver (e.g., Firefox, Edge, etc.)

try:
    # Navigate to a website
    driver.get("https://sanarais.online/test.php")

    # Find the body element and send "Hello, World!" to it
    body_element = driver.find_element_by_tag_name('body')
    body_element.send_keys("Hello, World!")

    # Wait for a few seconds to see the result
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
