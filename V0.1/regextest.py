#https://stackoverflow.com/questions/11475885/python-replace-regex
import re

string = "This is a really <script>Cancer</script> cool script"

print(re.sub('<script>.*</script>',"",string))