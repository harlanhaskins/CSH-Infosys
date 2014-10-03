import argparse
from boilerplate import *
from BetaBrite import WRITE_MODES
def files(headerID):
    fileID = int(headerID) + 1
    return (headerID, str(fileID))

def postTextToSign(text, fileInt, style):
    if not text:
        return
    textHeader, textFile = files(fileInt)
    update = False  
    
    if not server.fileExists(textHeader):
        server.addFile(textHeader)
        server.addText(textHeader, style, "%" + textFile, textFile)
        update = True

    if not server.fileExists(textFile):
        server.addFile(textFile)
        update = True

    server.addString(textFile, text)
    if update:
        server.updateSign() 
     

def validStyle(style):
    return style in WRITE_MODES

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Write custom text to infosys')
    parser.add_argument('text', help='Text to send to infosys')
    parser.add_argument('-s', '--style', help='The style of the text', default='ROTATE')
    parser.add_argument("-f", "--fileID", help="The file number you'd like.")
    args = parser.parse_args()
    text = args.text
     
    if args.fileID:
        fileID = args.fileID
    else:
        fileID = "40"

    try:
        fileInt = int(fileID)
    except ValueError:
        print("File must be an integer.")
   
    if not validStyle(args.style):
        print(args.style + ' is not a valid style, using ROTATE')
        args.style = 'ROTATE'
    
    postTextToSign(text, fileInt, args.style)    
         
