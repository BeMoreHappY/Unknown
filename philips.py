import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
import requests
from imap_tools import MailBox, AND, A, OR
from tkinter import *
import tkinter.messagebox
from kameleoo import Kameleo


def RetMessages(mailbox, where, subject):
    mailbox.folder.set(where)
    lista = []
    for msg in mailbox.fetch(AND(subject=[subject, subject.lower(), subject.upper(), subject.capitalize()])):
        lista.append(msg)
    return lista


def CheckTextIndex(text, what):
    i = 0
    for val in text:
        if val == what:
            return i
        i += 1


def GetText(msg):
    text = msg.html.encode('utf-8').decode('ascii', 'ignore').split()
    return text


def Button():
    root = tkinter.Tk()
    root.title("When you press a button the message will pop up")
    root.geometry('500x250')
    tkinter.messagebox.showinfo("phillips", "Nacisnij przycisk, aby przejsc dalej")
    root.destroy()
    root.mainloop()


def philipsBot(data, lock):
    kameleo = Kameleo(profile_id=data[8], path=data[7] + data[1] + ".kameleo")
    firstName = data[1].split(" ")[0]
    lastName = data[1].split(" ")[1]
    gender = "male"
    passwd = data[3]
    adres = data[4].split(":")
    ulica = adres[0]
    kodPocztowy = adres[1]
    miasto = adres[2]
    kameleo.startProfile()
    driver = kameleo.driver
    # # proxy = requests.get('http://192.168.1.2:9049/v1/ips?num=1&country=DE&state=all&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=').text
    # # option = uc.ChromeOptions()
    # # option.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    # # print(proxy)
    # # option.add_argument(f'--proxy-server=%s' % proxy)
    # driver = uc.Chrome()
    wait = WebDriverWait(driver, 20)
    # threading.Thread(target=akceptacja, args=(driver,)).start()
    driver.get("https://www.subscriptions.philips.de/de-de/checkout?bundle=lumea-BRP95800-m-17m&modified=true")
    wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "truste_popframe")))
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".call"))).click()
    driver.switch_to.parent_frame()
    changedSite = False
    currentUrl = driver.current_url
    while not changedSite:
        try:
            driver.find_element(By.CSS_SELECTOR, "div[class='createAccount'] button["
                                                 "class='AppButton']").click()
            if driver.current_url != currentUrl:
                changedSite = True
        except:
            continue
    lock.acquire()
    while True:
        try:
            with open('email.txt', "r") as f:
                line = f.readline().strip()
            dane = line.split(":")
            email = dane[0]
            passwdEmail = dane[1]
            MailBox('outlook.office365.com').login(email, passwdEmail)
            with open('email.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('email.txt', 'w') as fout:
                fout.writelines(data[1:])
            break
        except:
            with open('email.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('email.txt', 'w') as fout:
                fout.writelines(data[1:])
            continue
    lock.release()

    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "#capture_traditionalRegistration_emailAddress"))).send_keys(email)
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "#capture_traditionalRegistration_newPassword"))).send_keys(passwd)
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "#capture_traditionalRegistration_firstName"))).send_keys(firstName)
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "#capture_traditionalRegistration_lastName"))).send_keys(lastName)
    select_element = driver.find_element(By.CSS_SELECTOR, '#capture_traditionalRegistration_gender')
    select = Select(select_element)
    select.select_by_value(gender)
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button[listener='true']"))).click()
    # print(proxy)
    while True:
        with MailBox('outlook.office365.com').login(email, passwdEmail) as mailbox:
            lista = RetMessages(mailbox, 'Inbox', "Verifizieren Sie Ihre E-Mail-Adresse.")
            if len(lista) == 0:
                continue
            else:
                iter = 0
                text = GetText(lista[iter])
                index = CheckTextIndex(text, 'ist:')
                code = text[index + 1][8:14]
                print(code)
                break
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "#secondFactorCodeRegistrationInput"))).send_keys(code)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, "#submitSecondFactorCodeRegistrationButton"))).click()

    # with open('adresy.txt', "r") as f:
    #     line = f.readline()
    # dane = line.split(":")
    # ulica = dane[0]
    # kodPocztowy = dane[1]
    # miasto = dane[2]

    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "input[name='shippingAddress-addition']"))).send_keys(ulica)
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "input[name='shippingAddress-zipCode']"))).send_keys(kodPocztowy)
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, "input[name='shippingAddress-city']"))).send_keys(miasto)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[data-name='checkoutShippingAddress-updateButton']"))).click()
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, "div[id='payment-type-scheme'] h3[class='Accordion_title']"))).click()
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, ".multiselect__placeholder"))).click()

    with open('karty.txt', "r") as f:
        line = f.readline()
    dane = line.split(":")
    karta = dane[0]
    numerKarty = dane[1]
    data = dane[2]
    cvv = dane[3]

    wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[contains(text(),"%s")]' % karta))).click()

    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".AppButton.orange-button"))).click()

    wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "[title='Iframe für Kartennummer']")))
    wait.until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Kartennummer']"))).send_keys(
        numerKarty)
    driver.switch_to.parent_frame()
    wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "[title='Iframe für Ablaufdatum']")))
    wait.until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Ablaufdatum']"))).send_keys(
        data)
    driver.switch_to.parent_frame()
    wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "[title='Iframe für Sicherheitscode']")))
    wait.until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Sicherheitscode']"))).send_keys(
        cvv)
    driver.switch_to.parent_frame()
    wait.until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[name='holderName']"))).send_keys(
        "%s %s" % (firstName, lastName))

    wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "adyen-checkout__button__text")))
    print("done")

    Button()

    with open('karty.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('karty.txt', 'w') as fout:
        fout.writelines(data[1:])

    driver.quit()
    return
