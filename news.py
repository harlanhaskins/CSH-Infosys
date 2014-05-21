import argparse
import requests
from boilerplate import *

def topHeadline(apikey):
    parameters = {"section" : "news"}
    GUARDIAN_URL = "http://content.guardianapis.com/search"
    headlines = requests.get(GUARDIAN_URL, params=parameters).json()

    try:
        headline = headlines["response"]["results"][0]["webTitle"]
        headline = headline.encode('ascii', 'ignore')
        print (headline)
        return headline
    except KeyError:
        return None

def asciify(string):
    # remove non-ascii characters. whoops.
    asciifiedString = [char for char in string if ord(char) < 128]
    print asciifiedString
    return asciifiedString

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
