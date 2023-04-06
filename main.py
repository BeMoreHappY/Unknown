from selenium.webdriver.remote.webdriver import By
from kameleoo import Kameleo
import os
from selenium import webdriver
import germanNameGenerator as namegen
import time
import requests
from kameleo.local_api_client.models.problem_response_py3 import ProblemResponseException
from conditions import WaitForElementPresence, WaitForElementClicable, CodeFromEmail, RemoveFirstLineFile
from dataClass import Data

changeIP = False
if changeIP:
    proxy = requests.get(
        'http://192.168.1.2:9049/v1/ips?num=1&country=DE&state=all&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=').text.split(
        ":")
    IP = proxy[0]
    port = int(proxy[1])
else:
    IP = "192.168.1.2"
    port = 30000

metoda = 1  # 1 - start profil by profilName  2 - create profile

kamelObj = Kameleo()
if metoda == 1 or metoda == 2:
    if metoda == 1:
        profileName = "Ilse-Kirchner"
        try:
            kamelObj.loadProfile(f"C:\\Users\\Mati\\Desktop\\{profileName}.kameleo")
            print("Wczytuje profil z pliku")
            kamelObj.startProfile()
        except ProblemResponseException:
            if kamelObj.checkIDprofileByName(profileName) is not False:
                kamelObj.setProfile(kamelObj.checkIDprofileByName(profileName))
                print("Wczytuje profil z ID")
                kamelObj.startProfile()
    elif metoda == 2:
        Dane = Data()
        kamelObj.createProfile("".join(Dane.fullName().replace(" ", "-")), IP, port)
        kamelObj.startProfile()

    options = webdriver.ChromeOptions()
    options.add_experimental_option("kameleo:profileId", kamelObj.profile.id)
    driver = webdriver.Remote(
        command_executor=f'http://localhost:{kamelObj.port}/webdriver',
        options=options
    )

driver.get('https://filman.cc/premium')

while True:
    x = input("1 - Wylacz i zapisz   2 - Wylacz bez zapisu  3 - uruchom jeszcze raz 4 - Usuń profil")
    if x == '1':
        kamelObj.stopProfile()
        kamelObj.saveProfile()
        kamelObj.stopClient()
        break
    elif x == '2':
        kamelObj.stopProfile()
        kamelObj.stopClient()
        break
    elif x == '3':
        kamelObj.stopProfile()
        kamelObj.startProfile()
    elif x == '4':
        kamelObj.stopProfile()
        kamelObj.deleteProfile()
        kamelObj.stopClient()
        break
