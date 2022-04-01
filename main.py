from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import time
from selenium.webdriver.common.action_chains import ActionChains

chrome_driver_filepath = "/Users/jamestipping/Documents/Python practise/chromedriver"
url = "https://www.linkedin.com/jobs/search/?geoId=102454443&keywords=python%20developer&location=Singapore"
driver = webdriver.Chrome(chrome_driver_filepath)
driver.implicitly_wait(10)
driver.get(url)
password = "****"
username = "****"

try:
    sign_in_button = driver.find_element_by_class_name("cta-modal__primary-btn")
    sign_in_button.click()
except NoSuchElementException:
    print("Login button matching class 'cta-modal__primary-btn' could not be found")
    print("You may already be logged in")
#
try:
    input = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    input.send_keys(username)
    password.send_keys(password)
    password.send_keys(Keys.ENTER)
except NoSuchElementException:
    print("input or password field cannot be found")
    print("You may already be logged in")

# Finds each job on the Linkedin page
time.sleep(3)
jobs = driver.find_elements_by_class_name("jobs-search-results__list-item")
job_ids_to_apply_to = []

# As not all content is loaded before scrolling down and clicking, this loop clicks on each job to load all content
# The "id" of each job (eg ember420) is stored in a list, if it is possible to "Apply easily"
for job in jobs:
    title = job.find_element_by_css_selector('a')
    actions = ActionChains(driver)
    actions.move_to_element(title).click().perform()
    time.sleep(1)
    if "Apply easily" in job.text.splitlines():
        print("break")
        job_ids_to_apply_to.append(job.get_attribute("id"))
        print(job.get_attribute("id"))

print("sorting done")

# Loops through each job that can be easily applied to, in order to complete the submission steps
for job_id in job_ids_to_apply_to:
    # Clicks on title (clicking on the rectangular object can result in being directed to a separate webpage)
    # Locates apply button, clicks on it, and does the same for the submit button
    try:
        current_job = driver.find_element_by_id(job_id)
        title = current_job.find_element_by_css_selector("a")
        title.click()
        time.sleep(1)
        apply_button = driver.find_element_by_css_selector(".jobs-apply-button")
        apply_button.click()
        time.sleep(1)
        submit_button = driver.find_element_by_css_selector(".artdeco-button--primary")
        submit_button.click()
    # If this exception is raised, the job has already been applied to
    except NoSuchElementException:
        print("Job already applied for")
    # If this exception is raised, the job has a multi step application process.
    # Click on dismiss, and then discard to remove the mini window
    except ElementClickInterceptedException:
        print("Complex application - skipped")
        time.sleep(2)
        dismiss_button = driver.find_element_by_css_selector("button.artdeco-modal__dismiss")
        dismiss_button.click()
        time.sleep(2)
        discard_button = driver.find_element_by_css_selector("button.artdeco-modal__confirm-dialog-btn.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
        discard_button.click()

    # This "else" section was added to handle the mini window after successful submission of an application.
    # Without this, the program will have an error after one successful application submission.
    # However, adding this "else" section also results in errors, causing the program to crash.
    # Why does this else statement throw the program?
    else:
        time.sleep(2)
        dismiss_button = driver.find_element_by_css_selector("button.artdeco-modal__dismiss")
        dismiss_button.click()





