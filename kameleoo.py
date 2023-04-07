import time

from kameleo.local_api_client.kameleo_local_api_client import KameleoLocalApiClient
from kameleo.local_api_client.builder_for_create_profile import BuilderForCreateProfile
from kameleo.local_api_client.models.load_profile_request_py3 import LoadProfileRequest
from kameleo.local_api_client.models.save_profile_request_py3 import SaveProfileRequest
from kameleo.local_api_client.models.problem_response_py3 import ProblemResponseException
from kameleo.local_api_client.models.server_py3 import Server
from selenium import webdriver
import requests
import json
import io
import os


class Kameleo:
    path = None
    name = None
    profile = None
    client = None
    driver = None
    # [IP, Proxy]
    proxy = None

    def __init__(self, *, profileName=None, fullName=None, changeProxy=False, IP="192.168.1.2", proxyPort=30000,
                 port=5051, device_type='desktop', language="de-DE"):
        """

        :param profileName: For existing profile
        :param fullName: For create profile
        :param IP:
        :param proxyPort:
        :param port:
        :param device_type:
        :param language:
        """
        self.client = KameleoLocalApiClient(f'http://localhost:{port}')
        self.proxy = [IP, proxyPort]
        self.port = port
        if profileName is not None:
            self.path = f"C:\\Users\\Mati\\Desktop\\{profileName}.kameleo"
            self.name = profileName
            self.loadProfile(self.path)
        else:
            self.base_profiles = self.client.search_base_profiles(
                os_family="windows",
                device_type='desktop',
                language="de-DE"
            )
            if changeProxy:
                self.proxyChange()
            print(self.proxy)
            self.createProfile("".join(fullName.replace(" ", "-")), self.proxy[0], self.proxy[1])

    def createProfile(self, name, ip, port):
        create_profile_request = BuilderForCreateProfile \
            .for_base_profile(self.base_profiles[0].id) \
            .set_name(name) \
            .set_proxy('socks5', Server(host=ip, port=port)) \
            .set_recommended_defaults() \
            .build()
        self.profile = self.client.create_profile(body=create_profile_request)
        self.name = name
        self.path = f"C:\\Users\\Mati\\Desktop\\{name}.kameleo"
        print(f'Utworzono profil o ID - {self.profile.id}')
        self.saveInFile()

    def readProfile(self):
        self.client.list_profiles()

    def AllProfile(self):
        print(self.client.list_profiles())

    def setProfile(self, id):
        self.profile = self.client.read_profile(id)
        print(f'Ustawiono profil o ID - {self.profile.id}')

    def startProfile(self, id=None):
        if id is None:
            id = self.profile.id
        self.client.start_profile(id)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("kameleo:profileId", self.profile.id)
        self.driver = webdriver.Remote(
            command_executor=f'http://localhost:{self.port}/webdriver',
            options=options
        )
        print(f'Uruchomiono profil o ID - {id}')

    def stopProfile(self):
        self.client.stop_profile(self.profile.id)
        print(f'Wstrzymano profil o ID - {self.profile.id}')

    def stopClient(self):
        self.client.close()

    def saveProfile(self, path=None):
        if path is None:
            path = self.path
        self.client.save_profile(self.profile.id, body=SaveProfileRequest(path=path))
        print(f'Zapisano profil o ID - {self.profile.id}')

    def loadProfile(self, path):
        try:
            self.path = path
            self.profile = self.client.load_profile(body=LoadProfileRequest(path=path))
            print("Wczytuje profil z pliku")
        except ProblemResponseException:
            profileId = self.checkIDprofileByName(self.name)
            if profileId != False:
                self.setProfile(profileId)
                print("Wczytuje profil z ID")
        print(f'Załadowano profil o ID - {self.profile.id}')

    def deleteProfile(self):
        self.client.delete_profile(self.profile.id)
        print(f'Usunięto profil o ID - {self.profile.id}')

    def saveInFile(self):
        dictProfile = {}
        try:
            with open("profile.txt", "r") as f:
                dictProfile = json.load(f)
            with open("profile.txt", "w") as f:
                if self.name not in dictProfile:
                    dictProfile[self.name] = self.profile.id
                    json.dump(dictProfile, f)
                else:
                    if dictProfile[self.name] != self.profile.id:
                        print("ID nie są takie same")
        except (io.UnsupportedOperation, FileNotFoundError, json.JSONDecodeError):
            print("profile.txt nie istenie lub nie posiada żadnych profili. Tworzę plik.")
            with open("profile.txt", "w") as f:
                dictProfile[self.name] = self.profile.id
                json.dump(dictProfile, f, indent=4)

        print("Zapisano ID profilu")

    def checkIDprofileByName(self, name):
        with open("profile.txt", "r") as f:
            try:
                dictProfile = json.load(f)
                if name not in dictProfile:
                    print("Nie ma takiego profilu o podanej nazwie")
                    return False
                return dictProfile[name]
            except io.UnsupportedOperation:
                print("Nie ma takiego profilu o podanej nazwie")
                return False

    def proxyChange(self):
        self.proxy = requests.get(
            'http://192.168.1.2:9049/v1/ips?num=1&country=DE&state=all&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=').text.split(
            ":")
        print(f"Zmiana proxy na {self.proxy}")

