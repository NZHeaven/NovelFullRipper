import argparse
import requests
import pdfkit
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger, PdfFileReader
import os
import re
import logging

def HandleArguments():
    parser = argparse.ArgumentParser(description="Script to scrap NovelFull site and convert Desired Chapters to PDF")
    parser.add_argument('-u','--uri',help="Root URL",dest='uri',required=True)
    parser.add_argument('-c',help="Chapter Sub URL", dest='curi',required=True)
    return parser.parse_args()

def getNextChapter(content):
    regex = r"(/((.|\n)*?).html)"
    matches = re.search(regex,content)
    if(matches != None):
        return matches.group(0)
    
    return "/NoMatch.html"

def ScrapChapters(uri,curi):
    ChapterNumber = 1
    pageurl = uri+curi
    page = requests.get(pageurl)
    
    while page.status_code != 404:
        soup = BeautifulSoup(page.content,'html.parser')
        chapter = str(soup.find(id='chapter').prettify())
        NextChapter = getNextChapter(str(soup.find(id='next_chap').prettify()))
        title = "Chapter_" + str(ChapterNumber)
        location = "./Chapters/{0}.pdf"
        pdfkit.from_string(chapter, location.format(title))
        print (f"\r  Fetching Chapters: ({str(ChapterNumber)}:??)", end="")
        ChapterNumber += 1
        pageurl = uri + NextChapter
        print(pageurl)
        page = requests.get(pageurl)

    print("\n")

def GeneratePDFBook():
    print("Combining Chapters and Generating Book....")
    #Count Number of Files in chapters to Merge
    paths, dirs, files = next(os.walk('./Chapters'))
    file_count = len(files)

    #Merge PDFs
    mergedObject = PdfFileMerger()
    for fileNumber in range(1, file_count):
        Filename = f"./Chapters/Chapter_{fileNumber}.pdf"
        mergedObject.append(PdfFileReader(Filename),import_bookmarks=False)

    #write the changes
    mergedObject.write("Book.pdf")
    print("Book Created")

def cleanup():
    #Remove Chapter files from Temp Chapter Folder
    print("Cleaning up....")
    paths, dirs, files = next(os.walk('./Chapters'))
    for file in files:
        os.remove(f"./Chapters/{file}")

if __name__ == "__main__":
    args = HandleArguments()
    logging.getLogger("requests").setLevel(logging.WARNING)
    ScrapChapters(args.uri,args.curi)
    GeneratePDFBook()
    #cleanup()
    print("-------- Done :) ------")
