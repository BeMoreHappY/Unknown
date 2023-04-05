from selenium.webdriver.remote.webdriver import By
from kameleoo import Kameleo
import os
from selenium import webdriver
import germanNameGenerator as namegen
import time
import requests
from kameleo.local_api_client.models.problem_response_py3 import ProblemResponseException
from conditions import WaitForElementPresence, PickEmail, WaitForElementClicable, CodeFromEmail, RemoveFirstLineFile



changeIP = False
metoda = 2 #    1 - start profil by profilName  2 - create profile
profileName = "LauraSchulte"


kamelObj = Kameleo()
firstName = str(namegen.get_random_name()).strip()
lastName = str(namegen.get_random_familyname()).strip()
fullName = f'{firstName} {lastName}'
#email = PickEmail("email.txt")
email = ["Matiskatibusdhw@gmail.com","sadoiv@ios12"]
#RemoveFirstLineFile("email.txt")

print(kamelObj.port)
passwd = f'{fullName}1234'
if changeIP:
    proxy = requests.get('http://192.168.1.2:9049/v1/ips?num=1&country=DE&state=all&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=').text.split(":")
    IP = proxy[0]
    port = int(proxy[1])
else:
    IP = "192.168.1.2"
    port = 30000
publicIP = requests.get("https://api.ipify.org").text
allData = [publicIP, email, fullName, passwd]
print(allData)

if metoda == 1:
    try:
        kamelObj.loadProfile(f"C:\\Users\\Mati\\Desktop\\{profileName}.kameleo")
        kamelObj.startProfile()
    except ProblemResponseException:
        if kamelObj.checkIDprofileByName(profileName) is not False:
            kamelObj.setProfile(kamelObj.checkIDprofileByName(profileName))
            kamelObj.startProfile()

elif metoda == 2:
    kamelObj.createProfile("".join(fullName.replace(" ", "")), IP, port)
    kamelObj.startProfile()


options = webdriver.ChromeOptions()
options.add_experimental_option("kameleo:profileId", kamelObj.profile.id)
driver = webdriver.Remote(
    command_executor=f'http://localhost:{kamelObj.port}/webdriver',
    options=options
)

driver.get('https://filman.cc/premium')
print(driver.title)

x = input("")

kamelObj.stopProfile()
kamelObj.saveProfile()

kamelObj.startProfile()
x = input("")
kamelObj.stopProfile()
kamelObj.stopClient()


