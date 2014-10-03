import argparse
import pytumblr
import random
import json
from bs4 import BeautifulSoup
from boilerplate import server

rand = random.SystemRandom()

def getPost(client, user):
    info = client.blog_info(user)
    nposts = info['blog']['posts']

    postnum = rand.randint(0, nposts - 1)

    post = client.posts(user, offset = postnum, limit = 1)
    body = BeautifulSoup(post['posts'][0]['body'])
    return ' '.join(body.stripped_strings)

def getPostWithLimit(client, user, line_limit = 80):
    while True:
        post = getPost(client, user)
        if len(post) <= line_limit:
            return post

def postToSign(text, FILE_ID):
    if not server.fileExists(FILE_ID):
        server.addFile(FILE_ID)

    server.addText(FILE_ID, "ROTATE", text)

    server.updateSign()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Post to infosys from tumblr.')
    parser.add_argument("-u", "--user", help="tumblr user to read from")
    parser.add_argument("-f", "--fileID", help="the file number you'd like.")
    parser.add_argument("-c", "--credsFile", help="credentials file")
    args = parser.parse_args()

    if args.fileID:
        fileID = args.fileID
    else:
        fileID = "52"

    creds = json.loads(open(args.credsFile, "r").read())

    client = pytumblr.TumblrRestClient(
        creds['consumerKey'],
        creds['consumerSecret'],
        creds['oauthToken'],
        creds['oauthSecret']
    )

    postToSign(getPostWithLimit(client, args.user), fileID)
