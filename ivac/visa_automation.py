from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Function to read applicant data from a text file
def read_applicant_data(file_path):
    applicants = {}
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return applicants
    
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                applicants[key] = value
    return applicants

# Function to fill Application Info tab
def fill_application_info(driver, web_file_number):
    try:
        Select(driver.find_element(By.ID, "mission")).select_by_visible_text("Dhaka")
        driver.find_element(By.ID, "web_file_number").send_keys(web_file_number)
        driver.find_element(By.ID, "confirm_web_file_number").send_keys(web_file_number)
        Select(driver.find_element(By.ID, "ivac_center")).select_by_visible_text("IVAC, Dhaka (JFP)")
        Select(driver.find_element(By.ID, "visa_type")).select_by_visible_text("MEDICAL/MEDICAL ATTENDANT VISA")
        driver.find_element(By.ID, "save_and_next").click()
        print(f"Application Info filled for Web File: {web_file_number}")
    except Exception as e:
        print(f"Error in Application Info: {e}")

# Function to fill Personal Info tab
def fill_personal_info(driver, name, email, phone):
    try:
        driver.find_element(By.ID, "full_name").send_keys(name)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "phone").send_keys(phone)
        driver.find_element(By.ID, "save_and_show_overview").click()
        print(f"Personal Info filled for: {name}")
    except Exception as e:
        print(f"Error in Personal Info: {e}")

# Function to handle Overview tab
def handle_overview_tab(driver):
    try:
        driver.find_element(By.ID, "add_more_for_family").click()
        driver.find_element(By.ID, "terms_checkbox").click()
        driver.find_element(By.ID, "confirm_and_move_for_payment").click()
        print("Overview tab completed successfully.")
    except Exception as e:
        print(f"Error in Overview tab: {e}")

# Main Automation Flow
def automate_visa_application():
    applicants = read_applicant_data("applicants.txt")
    
    driver_path = r"I:\\1Automating Task\\ivac\\chromedriver.exe"
    if not os.path.exists(driver_path):
        print(f"Error: Chromedriver not found at {driver_path}")
        return
    
    service = Service(driver_path)
    try:
        driver = webdriver.Chrome(service=service)
        driver.get("https://payment.ivacbd.com")
        driver.maximize_window()
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return
    
    try:
        for i in range(1, 4):  # Assuming 3 applicants
            web_file_key = f"applicant_{i}_web_file"
            name_key = f"applicant_{i}_name"
            email_key = f"applicant_{i}_email"
            phone_key = f"applicant_{i}_phone"
            
            if web_file_key in applicants and name_key in applicants and email_key in applicants and phone_key in applicants:
                fill_application_info(driver, applicants[web_file_key])
                fill_personal_info(driver, applicants[name_key], applicants[email_key], applicants[phone_key])
                
                handle_overview_tab(driver)
        print("All applicants processed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(10)
        driver.quit()

# Run the automation
if __name__ == "__main__":
    automate_visa_application()
