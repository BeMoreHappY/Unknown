from kameleo.local_api_client.kameleo_local_api_client import KameleoLocalApiClient
from kameleo.local_api_client.builder_for_create_profile import BuilderForCreateProfile
from kameleo.local_api_client.models.load_profile_request_py3 import LoadProfileRequest
from kameleo.local_api_client.models.save_profile_request_py3 import SaveProfileRequest
from kameleo.local_api_client.models.server_py3 import Server
import os


class Kameleo:

    def __init__(self, port=5051, device_type='desktop', language="de-DE"):
        self.port = port
        self.client = KameleoLocalApiClient(f'http://localhost:{self.port}')
        self.base_profiles = self.client.search_base_profiles(
            device_type='desktop',
            language="de"
        )
        self.create_profile_request = None
        self.profile = None
        self.path = None
        self.name = None

    def createProfile(self, name, ip, port):
        create_profile_request = BuilderForCreateProfile \
            .for_base_profile(self.base_profiles[0].id) \
            .set_name(str(name)) \
            .set_proxy('socks5', Server(host=ip, port=port)) \
            .set_recommended_defaults() \
            .build()
        self.profile = self.client.create_profile(body=create_profile_request)
        self.name = name

    def setProfile(self, id):
        self.profile = self.client.read_profile(id)

    def startProfile(self):
        self.client.start_profile(self.profile.id)

    def stopProfile(self):
        self.client.stop_profile(self.profile.id)

    def saveProfile(self):
        path = f'{os.path.dirname(os.path.realpath(__file__))}\\{self.name}'
        self.client.save_profile(self.profile.id, body=SaveProfileRequest(path=path))

    def loadProfile(self, name):
        self.file = name
        path = f'{os.path.dirname(os.path.realpath(__file__))}\\{self.file}'
        print(path)
        self.profile = self.client.load_profile(body=LoadProfileRequest(path=path))

    def deleteProfile(self):
        self.client.delete_profile(self.profile.id)
