from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
from imap_tools import MailBox, AND, A, OR
from conditions import WaitForElementPresence, WaitForElementClicable


class Amazon:
    def __init__(self, driver):
        self.driver = driver

    def rejestracja(self, name, email, passwd):
        WaitForElementPresence(self.driver, 20, By.CSS_SELECTOR, "#ap_customer_name").send_keys(name)
        WaitForElementPresence(self.driver, 20, By.CSS_SELECTOR, "#ap_email").send_keys(email[0])
        WaitForElementPresence(self.driver, 20, By.CSS_SELECTOR, "#ap_password").send_keys(passwd)
        WaitForElementPresence(self.driver, 20, By.CSS_SELECTOR, "#ap_password_check").send_keys(passwd)
        WaitForElementClicable(self.driver, 20, By.CSS_SELECTOR, "#continue").click()
        # CodeFromEmail(email)

    def wyszukaj(self, item):
        WaitForElementPresence(self.driver, 20, By.CSS_SELECTOR, "#twotabsearchtextbox").send_keys(item + '\n')

    def chooseCategory(self, category):
        match category:
            case "PCs & Laptops":
                WaitForElementClicable(self.driver, 20, By.CSS_SELECTOR, ".hm-icon.nav-sprite").click()
                WaitForElementClicable(self.driver, 20, By.CSS_SELECTOR,
                                       "div[id='hmenu-container'] li:nth-child(18) a:nth-child(1) div:nth-child(1)").click()
                WaitForElementClicable(self.driver, 20, By.CSS_SELECTOR,
                                       "ul[class='hmenu hmenu-visible hmenu-translateX'] li:nth-child(16) a:nth-child(1)").click()

    def chooseTab(self, tab):
        match tab:
            case "Best Sellers":
                WaitForElementClicable(self.driver, 20, By.CSS_SELECTOR,
                                       ".nav-a[href='/-/en/gp/bestsellers/?ref_=nav_cs_bestsellers']").click()


