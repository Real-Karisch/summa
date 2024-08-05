import re

htmlSingleTagTranslations = {
    '  ': '<br>',
}

htmlRegionTagTranslations = [ #these will fill in the symbol with tag, and put the second capture group (if any) in the dynamic attribute
    {
        'symbol': '_',
        'tag': 'i',
        'dynamicAttribute': '',
        'staticAttributeStr': '',
    },
    {
        'symbol': '@',
        'tag': 'span',
        'dynamicAttribute': 'title',
        'staticAttributeStr': ' id="notation"',
    },
    {
        'symbol': '%',
        'tag': 'a',
        'dynamicAttribute': 'href',
        'staticAttributeStr': ' id="notation"',
    },
]

def formatStrToHtml(string):
    formatted = re.sub('  ', '<br>', string)
    return formatted

def htmlSingleTagTranslator(string):
    newString = string
    for pattern, replacement in htmlSingleTagTranslations.items():
        newString = re.sub(pattern, replacement, newString)
    
    return newString

def htmlRegionTagTranslator(string):
    stringList = list(string)
    for tagDetails in htmlRegionTagTranslations:
        

        if re.search(tagDetails['symbol'], string):
            pattern = f"{tagDetails['symbol']}([^#]*)#([^{tagDetails['symbol']}]*){tagDetails['symbol']}" if tagDetails['dynamicAttribute'] != '' else f"{tagDetails['symbol']}([^{tagDetails['symbol']}]*)(){tagDetails['symbol']}"
            matchCnt = 1
            for match in re.finditer(pattern, string):
                activeDynamicAttribute = tagDetails['dynamicAttribute'] != ''
                dynamicAttribute = f' {tagDetails["dynamicAttribute"]}="{match.group(2)}"' if activeDynamicAttribute else ''
                stringList[match.start()] = f"<{tagDetails['tag']}{dynamicAttribute}{tagDetails['staticAttributeStr']}>{match.group(1)}</{tagDetails['tag']}>"
                stringList[match.start()+1:match.end()] = [''] * (match.end() - match.start() - 1)
                matchCnt += 1

    newString = ''.join(stringList)
    return newString

def htmlTranslator(string):
    return htmlSingleTagTranslator(
        htmlRegionTagTranslator(string)
    )