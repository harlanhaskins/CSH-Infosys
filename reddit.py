import requests
import xmlrpclib
import re
import argparse

parser = argparse.ArgumentParser(description='Read from a subreddit.')
parser.add_argument("-r", "--subreddit", help="specify the subreddit from which to read.")

args = parser.parse_args()

if args.subreddit:
    subreddit = "/r/" + args.subreddit
else:
    subreddit = "/hot"

print subreddit

hotPosts = requests.get('http://www.reddit.com' + subreddit + '.json')

if subreddit == "/hot":
    subreddit = "Reddit"
print subreddit

posts = hotPosts.json()["data"]["children"]

title = ""
for post in posts:
    if not post["data"]["stickied"]:
        title = post['data']['title']
        break

title = re.sub(r'^[\[\(][fmFM][\]\)]\s+', '', title)
title = re.sub(r'\s+[\[\(][fmFM][\]\)]$', '', title)
title = re.sub(r'\s+[\[\(][fmFM][\]\)]\s+', ' ', title)
title = re.sub(r'[\[\(]([fmFM])[\]\)]', '\\1', title)

REDDIT_HEADER = "33"
REDDIT_FILE = "34"

server = xmlrpclib.ServerProxy("http://infosys.csh.rit.edu:8080")

flash = False

if not server.fileExists(REDDIT_HEADER):
    server.delFile(REDDIT_HEADER)
    server.addFile(REDDIT_HEADER)
    flash = True

    server.addText(REDDIT_HEADER, "ROTATE", "%" + REDDIT_FILE, REDDIT_FILE)

if not server.fileExists(REDDIT_FILE):
    server.delFile(REDDIT_FILE)
    server.addFile(REDDIT_FILE)
    flash = True

server.addString(REDDIT_FILE, title)

flash = bool(title) or flash

if flash:
    server.updateSign()
