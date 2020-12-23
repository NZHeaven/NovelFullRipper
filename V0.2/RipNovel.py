import argparse
# import requests
# import pdfkit
# from bs4 import BeautifulSoup
# from PyPDF2 import PdfFileMerger, PdfFileReader
# import os

def HandleArguments():
    parser = argparse.ArgumentParser(description="Script to scrap NovelFull site and convert Desired Chapters to PDF")
    parser.add_argument('-u','--uri',help="URL To Book",dest='uri',required=True)
    parser.add_argument('-start','--start_chapter',help="Chapter to start with, Defaults to 1",dest='start_chapter', default=1,type=int)
    parser.add_argument('-end','--end_chapter',help="Chapter to Stop at, Defaults to get all current chapters",dest="end_chapter",default=99999,type=int)
    return parser.parse_args()

def ScrapChapters(uri,start_chapter,end_chapter):
    URL = "https://novelfull.com/i-have-countless-legendary-swords/chapter-{0}.html"
    ChapterNumber = 32
    page = requests.get(URL.format(ChapterNumber))

    while page.status_code != 404:
        soup = BeautifulSoup(page.content,'html.parser')
        chapter = str(soup.find(id='chapter').prettify())
        title = "Chapter " + str(ChapterNumber)
        location = "./Chapters/{0}.pdf"
        pdfkit.from_file('test.html', location.format(title))
        ChapterNumber += 1
        page = requests.get(URL.format(ChapterNumber))

def RemoveScriptTags(chapter):
    regex = re.compile(r'(<script((.|\n)*?)<\/script>)')
    return re.sub(regex,"",chapter)

def GeneratePDFBook():
    #Count Number of Files in chapters to Merge
    paths, dirs, files = next(os.walk('./Chapters'))
    file_count = len(files)

    #Merge PDFs
    mergedObject = PdfFileMerger()
    for fileNumber in range(1, file_count):
        Filename = "./Chapters/Chapter {0}.pdf"
        mergedObject.append(PdfFileReader(Filename.format(fileNumber)))
    #write the changes
    mergedObject.write("Book.pdf")

if __name__ == "__main__":
    args = HandleArguments()
    ScrapChapters(args.uri,args.start_chapter,args.end_chapter)
    GeneratePDFBook()