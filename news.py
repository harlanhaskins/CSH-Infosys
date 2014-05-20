import argparse
import requests
import xmltodict
from boilerplate import *

def topHeadline(apikey):
    parameters = {"expired" : True,
                  "api_key" : apikey}
    USA_TODAY_URL = "http://api.usatoday.com/open/breaking"
    headlines = requests.get(USA_TODAY_URL, params=parameters)

    headlineDict = xmltodict.parse(headlines.text)
    try:
        headline = headlineDict["rss"]["channel"]["item"][0]["title"]
        print(headline)
        return headline
    except KeyError:
        return None

def postHeadlineToSign(headline):
    NEWS_HEADER = "22"
    NEWS_FILE = "23"

    update = False
    if not server.fileExists(NEWS_HEADER):
        server.addFile(NEWS_HEADER)
        server.addText(NEWS_HEADER, "ROTATE", 
                        "Top Headline: %" + NEWS_FILE, NEWS_FILE)
        update = True

    if not server.fileExists(NEWS_FILE):
        server.addFile(NEWS_FILE)
        update = True

    server.addString(NEWS_FILE, headline)

    if update:
        server.updateSign()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("apikey", help="The key used to authenticate")

    args = parser.parse_args()

    if not args.apikey:
        exit(0)

    title = topHeadline(args.apikey)
    if not title:
        exit(0)

    postHeadlineToSign(title)
