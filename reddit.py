import requests
import re
import argparse
from boilerplate import *

def normalizedSubreddit(subreddit):
    if subreddit:
        return "/r/" + subreddit
    else:
        return "/hot"

def topTitle(subreddit):
    try:
        hotPosts = requests.get('http://www.reddit.com' + subreddit + '.json')

        posts = hotPosts.json()["data"]["children"]

        title = ""
        for post in posts:
            if not post["data"]["stickied"]:
                title = post['data']['title']
                break

        return normalizedTitle(title)
    except KeyError:
        return None

def normalizedTitle(title):
    title = re.sub(r'^[\[\(][fmFM][\]\)]\s+', '', title)
    title = re.sub(r'\s+[\[\(][fmFM][\]\)]$', '', title)
    title = re.sub(r'\s+[\[\(][fmFM][\]\)]\s+', ' ', title)
    title = re.sub(r'[\[\(]([fmFM])[\]\)]', '\\1', title)
    return title

def files(headerID):
    fileID = int(headerID) + 1
    return (headerID, str(fileID))

def postTitleToSign(title, subreddit, REDDIT_HEADER, exclude_leadin=False):
    if not title:
        return

    REDDIT_HEADER, REDDIT_FILE = files(REDDIT_HEADER)
    update = False

    if not server.fileExists(REDDIT_HEADER):
        server.addFile(REDDIT_HEADER)
        server.addText(REDDIT_HEADER, "ROTATE", "%" + REDDIT_FILE, REDDIT_FILE)
        update = True

    if not server.fileExists(REDDIT_FILE):
        server.addFile(REDDIT_FILE)
        update = True

    if subreddit == "/hot":
        subreddit = "Reddit"

    if not exclude_leadin:
        title = "Top post from " + subreddit + ": " + title

    server.addString(REDDIT_FILE, title)

    if update:
      server.updateSign()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read from a subreddit.')
    parser.add_argument("-r", "--subreddit", help="specify the subreddit from which to read.")
    parser.add_argument("-l", "--exclude-leadin", 
                        help="Specifies that this subreddit will not be identified prior to display.", action="store_true")
    parser.add_argument("-f", "--fileID", help="The file number you'd like.")

    args = parser.parse_args()

    if args.fileID:
        fileID = args.fileID
    else:
        fileID = "34"

    try:
        fileInt = int(fileID)
    except ValueError:
        print("File must be an integer.")

    subreddit = normalizedSubreddit(args.subreddit)
    title = topTitle(subreddit)
    if not title:
        # print("title not found")
        exit(0)

    postTitleToSign(title, subreddit, fileID, exclude_leadin=args.exclude_leadin)

