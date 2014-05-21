from boilerplate import *
import requests

def topTitle():
    posts = requests.get("http://api.ihackernews.com/page")
    post = posts.json()["items"][0]
    title = post["title"]
    return title

def postTitleToSign(title):
    HN_HEADER = "60"
    HN_FILE   = "61"

    update = False

    if not server.fileExists(HN_HEADER):
        server.addFile(HN_HEADER)
        server.addText(HN_HEADER, "ROTATE", "Top Hacker News Post: %" + HN_FILE, HN_FILE)
        update = True

    if not server.fileExists(HN_FILE):
        server.addFile(HN_FILE)
        update = True

    server.addString(HN_FILE, title)

    if update:
        server.updateSign()

if __name__ == "__main__":
    title = topTitle()
    postTitleToSign(title)
