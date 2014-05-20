import argparse
import requests
import xmltodict
import xmlrpclib

def topHeadline(apikey):
    USA_TODAY_URL = "http://api.usatoday.com/open/breaking?expired=true&api_key=" + args.apikey
    headlines = requests.get(USA_TODAY_URL)

    headlineDict = xmltodict.parse(headlines.text)
    try:
        return headlineDict["rss"]["channel"]["item"][0]["title"]
    except KeyError:
        return None

def postHeadlineToSign(headline):
    NEWS_HEADER = "22"
    NEWS_FILE = "23"

    flash = False

    server = xmlrpclib.ServerProxy("http://infosys.csh.rit.edu:8080")

    if not server.fileExists(NEWS_HEADER):
        server.delFile(NEWS_HEADER)
        server.addFile(NEWS_HEADER)
        flash = True

        server.addText(NEWS_HEADER, "ROTATE", "Top Headline:")
        server.addText(NEWS_HEADER, "ROTATE", " %" + NEWS_FILE, NEWS_FILE)

    if not server.fileExists(NEWS_FILE):
        server.delFile(NEWS_FILE)
        server.addFile(NEWS_FILE)
        flash = True

    server.addString(NEWS_FILE, headline)

    if flash:
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
