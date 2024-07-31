import re
from copy import deepcopy

from variables import hardCodeLineAlterations, patterns

def alterSummaLines(summaLines, summaPartStr):
    copiedLines = deepcopy(summaLines)
    for overwrite in hardCodeLineAlterations[summaPartStr]['overwrites']:
        copiedLines[overwrite['index']] = overwrite['value']
    for substitution in hardCodeLineAlterations[summaPartStr]['substitutions']:
        copiedLines[substitution['index']] = re.sub(substitution['matchStr'], substitution['replaceStr'], copiedLines[substitution['index']])
    for insertion in hardCodeLineAlterations[summaPartStr]['insertions']:
        copiedLines.insert(insertion['index'], insertion['value'])
    for deleteRange in hardCodeLineAlterations[summaPartStr]['deleteRanges']:
        copiedLines = copiedLines[:deleteRange['indexStart']] + copiedLines[deleteRange['indexEnd']:]

    return copiedLines

def processQuestionIndices(questionLines):
    questionIndices = {
        'articleSeparators': [],
    }
    cnt = 0
    for line in questionLines:
        if re.search(patterns['lineSeparator'], line):
            questionIndices['articleSeparators'].append(cnt)
        cnt += 1
    return questionIndices

def processArticleIndices(articleLines):
    cnt = 0
    articleIndices = {
        'objectionStarts': [],
        'replyStarts': []
    }
    for line in articleLines:
        if re.search(patterns['objectionStart'], line):
            articleIndices['objectionStarts'].append(cnt)
        elif re.search(patterns['replyStart'], line):
            articleIndices['replyStarts'].append(cnt)
        elif re.search(patterns['sedContraStart'], line):
            articleIndices['sedContraStart'] = cnt
        elif re.search(patterns['respondeoStart'], line):
            articleIndices['respondeoStart'] = cnt
        cnt += 1

    return articleIndices

def processContentsIndices(contentsLines):
    contentsIndices = {
        'contentsQuestionsIndices': [],
        'nonEmptyNonQuestionIndices': [],
        'runningQuestionTypeCategory': {}
    }
    cnt = 0
    for line in contentsLines:
        #if re.search(patterns['emptyLines'], line):
        #    contentsIndices['runningQuestionTypeCategory'][cnt] = 'empty'
        if re.search(patterns['contentsQuestionLines'], line):
            contentsIndices['runningQuestionTypeCategory'][cnt] = 'question'
        elif re.search(patterns['continuedContentsQuestionLine'], line):
            contentsIndices['runningQuestionTypeCategory'][cnt] = 'continuedQuestion'
        elif re.search(patterns['allCaps'], line):
            contentsIndices['runningQuestionTypeCategory'][cnt] = 'sectionTitle'
        cnt += 1
    
    return contentsIndices