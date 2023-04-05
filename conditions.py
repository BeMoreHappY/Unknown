from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
from imap_tools import MailBox, AND, A, OR


def WaitForElementClicable(driver, time, by, value):
    return WebDriverWait(driver, time).until(EC.element_to_be_clickable((by, value)))


def WaitForElementPresence(driver, time, by, value):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((by, value)))


def FindElement(driver, by, value):
    return driver.find_element(by, value)


def URL_changed(driver, url):
    if driver.current_url != url:
        return True
    else:
        return False

def ReadFirstLineFile(path):
    with open(path, "r") as f:
        return f.readline()

def RemoveFirstLineFile(path):
    with open(path, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(path, 'w') as fout:
        fout.writelines(data[1:])

def CodeFromEmail(email):
    while True:
        with MailBox('outlook.office365.com').login(email[0], email[1]) as mailbox:
            lista = RetMessages(mailbox, 'Inbox', "Verifizieren Sie Ihre E-Mail-Adresse.")
            if len(lista) == 0:
                continue
            else:
                iter = 0
                text = GetText(lista[iter])
                index = CheckTextIndex(text, '(OTP):')
                code = text
                print(code)
                break

def CheckTextIndex(text, what):
    i = 0
    for val in text:
        if val == what:
            return i
        i += 1

def GetText(msg):
    text = msg.html.encode('utf-8').decode('ascii', 'ignore').split()
    return text

def RetMessages(mailbox, where, subject):
    mailbox.folder.set(where)
    lista = []
    for msg in mailbox.fetch(AND(subject=[subject, subject.lower(), subject.upper(), subject.capitalize()])):
        lista.append(msg)
    return lista
