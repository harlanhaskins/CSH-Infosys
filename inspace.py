import requests
from boilerplate import *

def numberOfPeopleInSpace():
    try:
        people = requests.get("http://www.howmanypeopleareinspacerightnow.com/space.json").json()
        number = people["number"]
        return number
    except KeyError:
        return None

def postNumberToSign(number):
    SPACE_HEADER = "82"
    SPACE_FILE   = "83"

    update = False
    if not server.fileExists(SPACE_HEADER):
        server.addFile(SPACE_HEADER)
        server.addText(SPACE_HEADER, "ROTATE", "There are %" + SPACE_FILE + " people in space right now.", SPACE_FILE)
        update = True

    if not server.fileExists(SPACE_FILE):
        server.addFile(SPACE_FILE)
        update = True

    server.addString(SPACE_FILE, str(number))

    if update:
        server.updateSign()

if __name__ == "__main__":
    number = numberOfPeopleInSpace()
    postNumberToSign(number)

