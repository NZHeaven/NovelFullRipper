#https://caendkoelsch.wordpress.com/2019/05/10/merging-multiple-pdfs-into-a-single-pdf/
#https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python

from PyPDF2 import PdfFileMerger, PdfFileReader
import os

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
