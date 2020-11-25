#https://stackoverflow.com/questions/11475885/python-replace-regex

#Regex That Worked
#https://stackoverflow.com/questions/16993795/regex-get-entire-string-between-two-keywords
#https://stackoverflow.com/questions/159118/how-do-i-match-any-character-across-multiple-lines-in-a-regular-expression/8269712
#https://regex101.com/r/1NnD9X/4/

import re
import pdfkit

regex = re.compile(r'(<script((.|\n)*?)<\/script>)')

f = open('test.html','r')
text = f.read()
f.close()

edit = re.sub(regex,"",text)

pdfkit.from_string(edit,'test.pdf')
w = open('test.txt','w')
w.write(edit)
w.write("</div>")
w.close()
