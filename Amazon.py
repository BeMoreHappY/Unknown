from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
from imap_tools import MailBox, AND, A, OR
from conditions import WaitForElementPresence, WaitForElementClicable


def rejestracja(driver, name, email, passwd):
    WaitForElementPresence(driver, 20, By.CSS_SELECTOR, "#ap_customer_name").send_keys(name)
    WaitForElementPresence(driver, 20, By.CSS_SELECTOR, "#ap_email").send_keys(email[0])
    WaitForElementPresence(driver, 20, By.CSS_SELECTOR, "#ap_password").send_keys(passwd)
    WaitForElementPresence(driver, 20, By.CSS_SELECTOR, "#ap_password_check").send_keys(passwd)
    WaitForElementClicable(driver, 20, By.CSS_SELECTOR, "#continue").click()
    # CodeFromEmail(email)