import re

def formatStrToHtml(string):
    formatted = re.sub('  ', '<br>', string)
    return formatted