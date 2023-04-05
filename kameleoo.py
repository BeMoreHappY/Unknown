import time

from kameleo.local_api_client.kameleo_local_api_client import KameleoLocalApiClient
from kameleo.local_api_client.builder_for_create_profile import BuilderForCreateProfile
from kameleo.local_api_client.models.load_profile_request_py3 import LoadProfileRequest
from kameleo.local_api_client.models.save_profile_request_py3 import SaveProfileRequest
from kameleo.local_api_client.models.server_py3 import Server
import json
import io
import os


class Kameleo:

    def __init__(self, port=5051, device_type='desktop', language="de-DE"):
        self.port = port
        self.client = KameleoLocalApiClient(f'http://localhost:{self.port}')
        self.base_profiles = self.client.search_base_profiles(
            os_family="windows",
            device_type='desktop',
            language="de-DE"
        )
        self.create_profile_request = None
        self.profile = None
        self.path = None
        self.name = None
        self.dictProfile = None

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
        print(self.profile, name)
        print(f'Utworzono profil o ID - {self.profile.id}')
        time.sleep(5)
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
        self.path = path
        self.profile = self.client.load_profile(body=LoadProfileRequest(path=path))
        print(f'Załadowano profil o ID - {self.profile.id}')

    def deleteProfile(self):
        self.client.delete_profile(self.profile.id)
        print(f'Usunięto profil o ID - {self.profile.id}')

    def saveInFile(self):
        self.dictProfile = {}
        try:
            with open("profile.txt", "r") as f:
                self.dictProfile = json.load(f)
            with open("profile.txt", "w") as f:
                if self.name not in self.dictProfile:
                    self.dictProfile[self.name] = self.profile.id
                    json.dump(self.dictProfile, f)
                else:
                    if self.dictProfile[self.name] != self.profile.id:
                        print("ID nie są takie same")
        except (io.UnsupportedOperation, FileNotFoundError, json.JSONDecodeError):
            print("profile.txt nie istenie lub nie posiada żadnych profili. Tworzę plik.")
            with open("profile.txt", "w") as f:
                self.dictProfile[self.name] = self.profile.id
                json.dump(self.dictProfile, f)

        print("Zapisano ID profilu")

    def checkIDprofileByName(self, name):
        with open("profile.txt", "r") as f:
            try:
                self.dictProfile = json.load(f)
                if name not in self.dictProfile:
                    print("Nie ma takiego profilu o podanej nazwie")
                    return False
                return self.dictProfile[name]
            except io.UnsupportedOperation:
                print("Nie ma takiego profilu o podanej nazwie")
                return False


