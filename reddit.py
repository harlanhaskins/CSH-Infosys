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

def postTitleToSign(title, subreddit, exclude_leadin=False, REDDIT_HEADER="33", REDDIT_FILE="34"):
    if not title:
        return

    server = xmlrpclib.ServerProxy("http://infosys.csh.rit.edu:8080")

    if server.fileExists(REDDIT_HEADER):
        server.delFile(REDDIT_HEADER)

    if server.fileExists(REDDIT_FILE):
        server.delFile(REDDIT_FILE)

    server.addFile(REDDIT_HEADER)
    server.addFile(REDDIT_FILE)

    if subreddit == "/hot":
        subreddit = "Reddit"

    if not exclude_leadin:
        leadin = "Top post from " + subreddit + ":"
        server.addText(REDDIT_HEADER, "HOLD", leadin, REDDIT_HEADER)
    server.addText(REDDIT_FILE, "ROTATE", title, REDDIT_FILE)

    server.updateSign()

def files(fileID):
    secondID = fileID + 1
    return (str(fileID), str(secondID))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read from a subreddit.')
    parser.add_argument("-r", "--subreddit", help="specify the subreddit from which to read.")
    parser.add_argument("-l", "--exclude-leadin", 
                        help="Specifies that this subreddit will not be identified prior to display.", action="store_true")
    parser.add_argument("-f", "--fileID", help="The file number you'd like (30-40)")

    args = parser.parse_args()

    if args.fileID:
        fileID = args.fileID
    else:
        fileID = "33"

    INVALID_FILE_ERROR = "File must be in range 30 - 39"

    try:
        fileInt = int(fileID)
    except ValueError:
        print(INVALID_FILE_ERROR)

    if not fileInt in range(30, 38):
        print(INVALID_FILE_ERROR)
        exit(0)

    headerID, fileID = files(fileInt)

    subreddit = normalizedSubreddit(args.subreddit)
    title = topTitle(subreddit)
    if not title:
        print("Title not found.")
        exit(0)

    postTitleToSign(title, subreddit, exclude_leadin=args.exclude_leadin, REDDIT_HEADER=headerID, REDDIT_FILE=fileID)

