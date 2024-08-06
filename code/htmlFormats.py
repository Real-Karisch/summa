import re

htmlSingleTagTranslations = {
    '  ': '<br>',
}

htmlRegionTagTranslations = [ #these will fill in the symbol with tag, and put the second capture group (if any) in the dynamic attribute
    {
        'symbol': '_',
        'tag': 'i',
        'dynamicAttributes': [],
        'staticAttributeStr': '',
    },
    {
        'symbol': '@',
        'tag': 'span',
        'dynamicAttributes': ['title'],
        'staticAttributeStr': ' id="notation"',
    },
    {
        'symbol': '%',
        'tag': 'a',
        'dynamicAttributes': ['href', 'title'],
        'staticAttributeStr': ' id="notationlink"',
    },
    {
        'symbol': '&',
        'tag': 'sup',
        'dynamicAttributes': ['title'],
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
            pattern = tagDetails['symbol']
            for _ in tagDetails['dynamicAttributes']:
                pattern += f"([^#]*)#"
            pattern += f"([^{tagDetails['symbol']}]*)" + tagDetails['symbol']
            #pattern = f"{tagDetails['symbol']}([^#]*)#([^{tagDetails['symbol']}]*){tagDetails['symbol']}" if tagDetails['dynamicAttribute'] != '' else f"{tagDetails['symbol']}([^{tagDetails['symbol']}]*)(){tagDetails['symbol']}"
            matchCnt = 1
            for match in re.finditer(pattern, string):
                activeDynamicAttribute = tagDetails['dynamicAttributes'] != []
                dynamicAttributeStr = ''
                groupCnt = 2
                for dynamicAttributeTag in tagDetails['dynamicAttributes']:
                    dynamicAttributeStr += f' {dynamicAttributeTag}="{match.group(groupCnt)}"'
                    groupCnt += 1
                stringList[match.start()] = f"<{tagDetails['tag']}{dynamicAttributeStr}{tagDetails['staticAttributeStr']}>{match.group(1)}</{tagDetails['tag']}>"
                stringList[match.start()+1:match.end()] = [''] * (match.end() - match.start() - 1)
                matchCnt += 1

    newString = ''.join(stringList)
    return newString

def htmlTranslator(string):
    return htmlSingleTagTranslator(
        htmlRegionTagTranslator(string)
    )