import germanNameGenerator as namegen
from conditions import RemoveFirstLineFile, ReadFirstLineFile
from imap_tools import MailBox, AND, A, OR


class Data:
    firstName = None
    lastName = None
    email = None
    passwd = None

    def __init__(self):
        self.firstName = self.firstNamefunc()
        self.lastName = self.lastNamefunc()

    def firstNamefunc(self):
        return namegen.get_random_name().strip()

    def lastNamefunc(self):
        return str(namegen.get_random_familyname()).strip()

    def fullName(self):
        return f'{self.firstName} {self.lastName}'

    def PickEmail(path):
        while True:
            try:
                line = ReadFirstLineFile(path)
                if not line.strip():
                    raise Exception("Nie ma emaili!")
                dane = line.split(":")
                MailBox('outlook.office365.com').login(dane[0], dane[1])
                return dane
            except:
                RemoveFirstLineFile(path)
                continue

    @staticmethod
    def genFullName():
        return f'{namegen.get_random_name()} {namegen.get_random_familyname()}'
