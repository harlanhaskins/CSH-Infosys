import requests
import xmlrpclib
import re
import argparse

def normalizedSubreddit(subreddit):
    if subreddit:
        return "/r/" + subreddit
    else:
        return "/hot"

def topTitle(subreddit):
    hotPosts = requests.get('http://www.reddit.com' + subreddit + '.json')

    posts = hotPosts.json()["data"]["children"]

    title = ""
    for post in posts:
        if not post["data"]["stickied"]:
            title = post['data']['title']
            break

    return normalizedTitle(title)

def normalizedTitle(title):
    title = re.sub(r'^[\[\(][fmFM][\]\)]\s+', '', title)
    title = re.sub(r'\s+[\[\(][fmFM][\]\)]$', '', title)
    title = re.sub(r'\s+[\[\(][fmFM][\]\)]\s+', ' ', title)
    title = re.sub(r'[\[\(]([fmFM])[\]\)]', '\\1', title)
    return title

def postTitleToSign(title):
    REDDIT_HEADER = "33"
    REDDIT_FILE = "34"

    server = xmlrpclib.ServerProxy("http://infosys.csh.rit.edu:8080")

    update_sign = False

    if not server.fileExists(REDDIT_HEADER):
        server.delFile(REDDIT_HEADER)
        server.addFile(REDDIT_HEADER)
        update_sign = True

        server.addText(REDDIT_HEADER, "ROTATE", "%" + REDDIT_FILE, REDDIT_FILE)

    if not server.fileExists(REDDIT_FILE):
        server.delFile(REDDIT_FILE)
        server.addFile(REDDIT_FILE)
        update_sign = True

    server.addString(REDDIT_FILE, title)

    if title or update_sign:
        server.updateSign()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read from a subreddit.')
    parser.add_argument("-r", "--subreddit", help="specify the subreddit from which to read.")
    parser.add_argument("-l", "--exclude-lead", 
                        help="Specifies that this subreddit will not be identified prior to display.", action="store_true")

    args = parser.parse_args()

    subreddit = normalizedSubreddit(args.subreddit)
    title = topTitle(subreddit)
    if not title:
        exit(0)
    postTitleToSign(title)

