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
    parser.add_argument('-u','--uri',help="URL To Book",dest='uri',required=True)
    parser.add_argument('-start','--start_chapter',help="Chapter to start with, Defaults to 1",dest='start_chapter', default=1,type=int)
    parser.add_argument('-end','--end_chapter',help="Chapter to Stop at, Defaults to get all current chapters",dest="end_chapter",default=99999,type=int)
    return parser.parse_args()

def ScrapChapters(uri,start_chapter,end_chapter):
    ChapterNumber = start_chapter
    page = requests.get(uri.format(ChapterNumber))

    while page.status_code != 404 and ChapterNumber <= end_chapter:
        soup = BeautifulSoup(page.content,'html.parser')
        chapter = str(soup.find(id='chapter').prettify())
        title = "Chapter_" + str(ChapterNumber)
        location = "./Chapters/{0}.pdf"
        pdfkit.from_string(RemoveScriptTags(chapter), location.format(title))
        print (f"\r  Fetching Chapters: ({str(ChapterNumber)}:??)", end="")
        ChapterNumber += 1
        page = requests.get(uri.format(ChapterNumber))

    print("\n")

def RemoveScriptTags(chapter):
    regex = re.compile(r'(<script((.|\n)*?)<\/script>)')
    return re.sub(regex,"",chapter)

def GeneratePDFBook(start_chapter):
    print("Combining Chapters and Generating Book....")
    #Count Number of Files in chapters to Merge
    paths, dirs, files = next(os.walk('./Chapters'))
    file_count = len(files)

    #Merge PDFs
    mergedObject = PdfFileMerger()
    for fileNumber in range(start_chapter, file_count):
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
    ScrapChapters(args.uri,args.start_chapter,args.end_chapter)
    GeneratePDFBook(args.start_chapter)
    cleanup()
    print("-------- Done :) ------")
