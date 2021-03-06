from boilerplate import *
import requests

def nextPun():
    try:
        pun = requests.get("http://san.csh.rit.edu:4200/next")
        punText = pun.json()["tweet"]["content"]
        if type(punText) == unicode:
            punText = punText.decode('ascii', 'ignore')
        return punText

    except:
        return None

def postPunToSign(pun):
    PUN_HEADER = "44"
    PUN_FILE = "45"

    update = False
    if not server.fileExists(PUN_HEADER):
        server.addFile(PUN_HEADER)
        server.addText(PUN_HEADER, "ROTATE", "Next 420 Pun: %" + PUN_FILE, PUN_FILE)
        update = True

    if not server.fileExists(PUN_FILE):
        server.addFile(PUN_FILE)
        update = True

    server.addString(PUN_FILE, pun)

    if update:
        server.updateSign()

if __name__ == "__main__":
    pun = nextPun()
    if not pun:
        exit(0)
    postPunToSign(pun)
