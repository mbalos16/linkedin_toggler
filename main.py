import argparse
import json
import logging
import logging.config
import sys
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Configure logger
def log_except_hook(*exc_info):
    logger = logging.getLogger(__name__)
    text = "".join(traceback.format_exception(*exc_info))
    logger.critical(f"Unhandled exception:\n{text}")


sys.excepthook = log_except_hook

logging.config.fileConfig(fname="logging.ini")
logger = logging.getLogger(__name__)


def load_secrets():
    logger.info("Loading secrets json.")
    f = open("secrets.json")
    secrets = json.load(f)
    f.close()
    logger.info("Secrets loaded successfully.")
    return secrets


def open_driver():
    """Open the Firefox driver.

    Returns:
        WebDriver: the driver instanced to be used in other function.
    """
    logger.info("Opening Firefox driver.")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.linkedin.com/feed/")
    logger.info("Firefox driver opened successfully.")
    return driver


def close_driver(driver):
    """Close the Firefox driver.

    Args:
        driver (WebDriver): the driver instanced to be used in other function.
    """
    driver.quit()
    logger.info("Driver closed.")


def login_linkedin(driver, username, password):
    """This function will login the user with the provided username and password.

    Args:
        driver (WebDriver): the driver instanced to be used in other function.
        username (str): The user's email for the LInkedIn profile.
        password (str): The user's password for the LinkedIn profile.
    """
    logger.info("Loggin to LinkedIn started.")
    # Go to the LInkedIn Login page
    driver.get("https://www.linkedin.com/login")
    logger.info("Switched to login page.")

    # Accept cookies
    accept_btn_xpath = "/html/body/div/main/div[1]/div/section/div/div[2]/button[1]"
    accept_btn = driver.find_element(by=By.XPATH, value=accept_btn_xpath)
    accept_btn.click()

    # Insert email
    email_id = "username"
    email_locator = driver.find_element(by=By.ID, value=email_id).send_keys(username)

    # Insert password
    pass_id = "password"
    pass_locator = driver.find_element(by=By.ID, value=pass_id).send_keys(password)

    # Press SignIn btn
    sign_in_btn_container_class = "login__form_action_container"
    sign_in_btn_parent = driver.find_element(
        by=By.CLASS_NAME, value=sign_in_btn_container_class
    )
    sign_in_btn = sign_in_btn_parent.find_element(by=By.XPATH, value="./button")
    sign_in_btn.click()
    logger.info("Logged in successfully.")


def is_work_status_open(driver):
    """Checks if the LinkedIn status is open.

    Args:
        driver (WebDriver): the driver instanced to be used in other function.

    Returns:
        bool: Returns True if the LinkedIn status is OpenToWork and False if is not.
    """
    logger.info("Checking LinkedIn status.")
    # Access the profile page
    driver.get("https://www.linkedin.com/in/me/")

    # Check the status
    photo_btn_class = "profile-photo-edit__edit-btn"
    photo_parent = driver.find_element(by=By.CLASS_NAME, value=photo_btn_class)
    content = photo_parent.get_attribute("innerHTML")
    open_status = "#OPEN_TO_WORK" in content
    logger.info(f"The LinkedIn status is {'open' if open_status else 'closed'}.")
    return open_status


def open_status(driver):
    """This function will turn the status on, adding the frame OpenToWork frame.

    Args:
        driver (WebDriver): the driver instanced to be used in other function.
    """
    logger.info("Opening LinkedIn status.")
    # Go to the profile page
    logger.info("Going to the profile page.")
    driver.get("https://www.linkedin.com/in/me/")

    # Open the image menu
    logger.info("Opening the image menu.")
    photo_btn_class = "profile-photo-edit__edit-btn"
    photo_btn = driver.find_element(by=By.CLASS_NAME, value=photo_btn_class)
    photo_btn.click()

    # Click on frames
    frames_parent_class = "imgedit-profile-photo-frame-viewer__actions"
    frames_parent = driver.find_element(by=By.CLASS_NAME, value=frames_parent_class)
    frame_btn = frames_parent.find_element(by=By.XPATH, value="./button[position()=3]")
    frame_btn.click()

    # Click on OpenToWork frame
    original_frame_btn_xpath = "//ul[contains(@class, 'imgedit-profile-frame-selector__frames')]/li[position()=2]/button"
    original_frame_btn = driver.find_element(
        by=By.XPATH, value=original_frame_btn_xpath
    )
    original_frame_btn.click()

    # Apply btn
    apply_btn_xpath = (
        "//div[contains(@class, 'imgedit-profile-frame-selector__actions')]/button"
    )
    apply_btn = driver.find_element(by=By.XPATH, value=apply_btn_xpath)
    apply_btn.click()

    # Location type
    loc_type_btns_xpath = "//fieldset[contains(@id, 'pill-form-component-openToWorkPreferencesFormElement-WORKPLACES')]/button"
    loc_type_btns = driver.find_elements(by=By.XPATH, value=loc_type_btns_xpath)
    for button in loc_type_btns:
        if "artdeco-pill--selected" not in button.get_attribute("outerHTML"):
            button.click()

    # Find and add locations on site
    LOCATIONS = ["London", "Royston"]

    for location in LOCATIONS:
        # When selecting remote location in the previous step, a new section is added to the form and that takes few miliseconds.
        # Similarly happens when a new location is added - it is displayed after few miliseconds.
        # Then the following sleep is required to prevent the location textbox from disappearing due to the delayed HTML updates.
        time.sleep(1)
        add_loc_btns_xpath = "//fieldset[contains(@id, 'pill-form-component-openToWorkPreferencesFormElement-JOB-LOCATIONS')]/div/button"
        loc_on_site = driver.find_element(by=By.XPATH, value=add_loc_btns_xpath)
        loc_on_site.click()
        location_class = "typeahead-cta__input"
        location_input = driver.find_element(by=By.CLASS_NAME, value=location_class)
        location_input.send_keys(location)
        # The following sleep is necessary for LinkedIn to fill the locations matching with the inserted one.
        time.sleep(3)
        location_input.send_keys(Keys.DOWN)
        location_input.send_keys(Keys.ENTER)
    # The following sleep is there for the same reason as the first sleep in the above for loop.
    time.sleep(1)

    # Start date: inmediatly available
    start_btns_xpath = "//fieldset[contains(@id, 'radio-button-form-component-openToWorkPreferencesFormElement-START-DATE')]/div[position()=1]/label"
    start_btn = driver.find_element(by=By.XPATH, value=start_btns_xpath)
    start_btn.click()

    # Employment type
    employment_type_btns_xpath = "//fieldset[contains(@id, 'pill-form-component-openToWorkPreferencesFormElement-JOB-TYPES')]/button"
    employment_type_btns = driver.find_elements(
        by=By.XPATH, value=employment_type_btns_xpath
    )
    for button in employment_type_btns:
        if "artdeco-pill--selected" not in button.get_attribute("outerHTML"):
            button.click()

    # Visibility: All LinkedIn members
    visibility_btns_xpath = "//fieldset[contains(@id, 'radio-button-form-component-openToWorkPreferencesFormElement-VISIBILITY')]/div[position()=2]/label"
    visibility_btn = driver.find_element(by=By.XPATH, value=visibility_btns_xpath)
    visibility_btn.click()

    # Save
    save_btn_xpath = "//div[contains(@id, 'artdeco-modal-outlet')]//button"
    save_btn = driver.find_elements(by=By.XPATH, value=save_btn_xpath)[-1]
    save_btn.click()
    logger.info("LinkedIn profile open successfully.")


def close_status(driver):
    """This function will turn the OpenToWork status off, removing the frame

    Args:
        driver (WebDriver): the driver instanced to be used in other function.
    """
    logger.info("Closing LInkedIn status.")

    # Go to the profile page
    logger.info("Going to the profile page.")
    driver.get("https://www.linkedin.com/in/me/")

    # Open the image menu
    logger.info("Opening the image menu.")
    photo_btn_class = "profile-photo-edit__edit-btn"
    photo_btn = driver.find_element(by=By.CLASS_NAME, value=photo_btn_class)
    photo_btn.click()

    # Click on frames
    frames_parent_class = "imgedit-profile-photo-frame-viewer__actions"
    frames_parent = driver.find_element(by=By.CLASS_NAME, value=frames_parent_class)
    frame_btn = frames_parent.find_element(by=By.XPATH, value="./button[position()=3]")
    frame_btn.click()

    # Click on Original frame
    original_frame_btn_xpath = "//ul[contains(@class, 'imgedit-profile-frame-selector__frames')]/li[position()=1]/button"
    original_frame_btn = driver.find_element(
        by=By.XPATH, value=original_frame_btn_xpath
    )
    original_frame_btn.click()

    # Apply btn
    apply_btn_xpath = (
        "//div[contains(@class, 'imgedit-profile-frame-selector__actions')]/button"
    )
    apply_btn = driver.find_element(by=By.XPATH, value=apply_btn_xpath)
    apply_btn.click()

    # Checkbox
    checkbox_input_xpath = "//fieldset[contains(@class, 'remove-frame-modal__image-container')]/label[position()=1]"
    checkbox_input = driver.find_element(by=By.XPATH, value=checkbox_input_xpath)
    checkbox_input.click()

    # Submit
    submit_btn_xpath = (
        "//footer[contains(@class, 'remove-frame-modal__actions')]/button[position()=2]"
    )
    submit_btn = driver.find_element(by=By.XPATH, value=submit_btn_xpath)
    submit_btn.click()
    logger.info("LinkedIn profile closed successfully.")


def parse_args():
    params = argparse.ArgumentParser(
        usage=(
            "This script is intended to access the LinkedIn status and check it and change it based on the day of the week."
        )
    )
    params.add_argument(
        "--open",
        action="store_true",
        help=(
            "If provided, the script will select the open to work frame in LinkedIn."
        ),
    )
    params.add_argument(
        "--close",
        action="store_true",
        help=("The script will select the original frame in LinkedIn."),
    )

    args = params.parse_args()

    if args.open and args.close:
        error_message = (
            "Both args.open and args.close are True, this is not a valid combination."
        )
        raise ValueError(error_message)

    if (args.open == False) and (args.close == False):
        error_message = (
            "Both args.open and args.close are False, this is not a valid combination."
        )
        raise ValueError(error_message)

    return args


if __name__ == "__main__":
    args = parse_args()

    driver = open_driver()
    driver.implicitly_wait(10)
    secrets = load_secrets()
    username = secrets["email"]
    password = secrets["pass"]
    login_linkedin(driver, username, password)
    is_open = is_work_status_open(driver)

    if args.open:
        if is_open:
            logger.info("The LinkedIn account is alredy open. Aborting mission...")
            close_driver(driver)
        else:
            logger.info("The LinkedIn account is closed. Openning...")
            open_status(driver)
            close_driver(driver)

    if args.close:
        if not is_open:
            logger.info("The LinkedIn account is alredy closed. Aborting mission...")
            close_driver(driver)
        else:
            logger.info("The LinkedIn account is open. Closing...")
            close_status(driver)
            close_driver(driver)
