import argparse
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def load_secrets():
    f = open("secrets.json")
    secrets = json.load(f)
    f.close()
    return secrets


def open_driver():
    """Open the Firefox driver.

    Returns:
        WebDriver: the driver instanced to be used in other function.
    """
    driver = webdriver.Firefox()
    driver.get("https://www.linkedin.com/feed/")
    return driver


def close_driver(driver):
    """Close the Firefos driver.

    Args:
        driver (WebDriver): the driver instanced to be used in other function.
    """
    print(type(driver))
    driver.quit()


def login_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")

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


def is_work_status_open(driver):
    # Access the profile page
    driver.get("https://www.linkedin.com/in/me/")

    # Check the status
    photo_btn_class = "profile-photo-edit__edit-btn"
    photo_parent = driver.find_element(by=By.CLASS_NAME, value=photo_btn_class)
    content = photo_parent.get_attribute("innerHTML")
    return "#OPEN_TO_WORK" in content


def open_status():
    pass


def close_status(driver):
    driver.get("https://www.linkedin.com/in/me/")

    # Open the image menu
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
    save_btn_xpath = (
        "//footer[contains(@class, 'remove-frame-modal__actions')]/button[position()=2]"
    )
    save_btn = driver.find_element(by=By.XPATH, value=save_btn_xpath)
    save_btn.click()


def parse_args():
    params = argparse.ArgumentParser(
        usage=(
            "This script is intended to access the LinkedIn status and check it and change it based on the day of the week."
        )
    )


if __name__ == "__main__":
    driver = open_driver()
    secrets = load_secrets()
    username = secrets["email"]
    password = secrets["pass"]
    login_linkedin(driver, username, password)
    is_open = is_work_status_open(driver)
    close_status(driver)
    # close_driver(driver)
