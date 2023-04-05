from selenium.webdriver.remote.webdriver import By
from kameleoo import Kameleo
import os
from selenium import webdriver
import germanNameGenerator as namegen
import time
import requests
from conditions import WaitForElementPresence, PickEmail, WaitForElementClicable, CodeFromEmail, RemoveFirstLineFile


try:
    changeIP = False
    kamelObj = Kameleo()
    name = namegen.get_random_name()
    #email = PickEmail("email.txt")
    email = ["Matiskatibusdhw@gmail.com","sadoiv@ios12"]
    #RemoveFirstLineFile("email.txt")

    print(kamelObj.port)
    passwd = f'{name}1234'
    if changeIP:
        proxy = requests.get('http://192.168.1.2:9049/v1/ips?num=1&country=DE&state=all&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=').text.split(":")
        IP = proxy[0]
        port = int(proxy[1])
    else:
        IP = "192.168.1.2"
        port = 30000
    publicIP = requests.get("https://api.ipify.org").text
    allData = [publicIP, email, name, passwd]
    print(allData)

    kamelObj.setProfile("dfb7717e-4a76-40e8-a6b9-338ad04d76aa")
    kamelObj.startProfile()

    options = webdriver.ChromeOptions()
    options.add_experimental_option("kameleo:profileId", kamelObj.profile.id)
    driver = webdriver.Remote(
        command_executor=f'http://localhost:{kamelObj.port}/webdriver',
        options=options
    )

    driver.get('https://www.nulled.to/topic/1483146-eset-nod32-antivirus-04172023/')
    print(driver.title)

    time.sleep(20)

    kamelObj.stopProfile()
    kamelObj.saveProfile()
except:
    kamelObj.stopProfile()
    kamelObj.saveProfile()

