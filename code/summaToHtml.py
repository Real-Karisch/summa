import re
from airium import Airium
from copy import deepcopy
import os

from variables import summaParts, hardCodeLineAlterations, patterns
from utils import processArticleIndices, processContentsIndices, processQuestionIndices, alterSummaLines

def parseObjections(articleLines, objectionStarts, objectionEnd):
    objIndices = objectionStarts + [objectionEnd]
    objections = {}
    for i in range(len(objectionStarts)):
        objectionLines = articleLines[objIndices[i]:objIndices[i+1]]
        objectionFirstLineSearch = re.search(patterns['objectionStart'], objectionLines[0])
        objectionNum = int(objectionFirstLineSearch.group(2))
        objectionFirstLineText = objectionFirstLineSearch.group(3)
        objectionLines[0] = objectionFirstLineText
        objections[objectionNum] = objectionLines
    return objections

def parseReplies(articleLines, replyStarts):
    replyStarts = replyStarts + [len(articleLines)]
    replies = {}
    for i in range(len(replyStarts) - 1):
        replyLines = articleLines[replyStarts[i]:replyStarts[i+1]]
        replyFirstLineSearch = re.search(patterns['replyStart'], replyLines[0])
        replyNum = int(replyFirstLineSearch.group(1))
        replyFirstLineText = replyFirstLineSearch.group(2)
        replyLines[0] = replyFirstLineText
        replies[replyNum] = replyLines
    return replies

def parseArticle(articleLines):
    #print(articleLines[0])
    articleIndices = processArticleIndices(articleLines)

    articleParsed = {}
    articleParsed['articleNum'] = re.search(patterns['articleFirstLine'], articleLines[0]).group(1)
    #articleParsed['articleTitle'] = f"{articleLines[0].strip()}: {articleLines[2]}"

    noSedContra = 'sedContraStart' not in articleIndices.keys()
    noRespondeo = 'respondeoStart' not in articleIndices.keys()
    noReplies = articleIndices['replyStarts'] == []

    if noSedContra:
        if noRespondeo:
            objectionEnd = articleIndices['replyStarts'][0]
        else:
            objectionEnd = articleIndices['respondeoStart']
    else:
        objectionEnd = articleIndices['sedContraStart']

    articleParsed['objections'] = parseObjections(
        articleLines=articleLines,
        objectionStarts=articleIndices['objectionStarts'],
        objectionEnd=objectionEnd
    )
    articleParsed['replies'] = parseReplies(
        articleLines=articleLines,
        replyStarts=articleIndices['replyStarts']
    )

    if noSedContra:
        articleParsed['sedContra'] = []
    else:
        if noRespondeo:
            if noReplies:
                articleParsed['sedContra'] = articleLines[articleIndices['sedContraStart']:]
            else:
                articleParsed['sedContra'] = articleLines[articleIndices['sedContraStart']:articleIndices['replyStarts'][0]]
        else:
            articleParsed['sedContra'] = articleLines[articleIndices['sedContraStart']:articleIndices['respondeoStart']]

    if noRespondeo:
        articleParsed['respondeo'] = []
    else:
        if noReplies:
            articleParsed['respondeo'] = articleLines[articleIndices['respondeoStart']:]
        else:
            articleParsed['respondeo'] = articleLines[articleIndices['respondeoStart']:articleIndices['replyStarts'][0]]
    articleParsed['articleTitle'] = f"{articleLines[0].strip()}: {''.join(articleLines[1:articleIndices['objectionStarts'][0]])}"

    return articleParsed

def parseSumma(summaLines):
    cnt = 0
    summaParsed = {}
    lineSeparators = []
    questionStarts = []
    for line in summaLines:
        if re.search(patterns['lineSeparator'], line):
            lineSeparators.append(cnt)
        elif  re.search(patterns['questionStart'], line):
            questionStarts.append(cnt)
        elif re.search(patterns['lastLine'], line):
            lastLine = cnt
        cnt += 1

    questionBookends = questionStarts + [lastLine]

    questionsLines = []
    for i in range(len(questionBookends)-1):
        #print(i)
        questionsLines.append(
            summaLines[questionBookends[i]:questionBookends[i+1]-2]
        )

    summaParsed['contentsLines'] = summaLines[lineSeparators[2]+2:lineSeparators[3]]
    summaParsed['questionsLines'] = questionsLines
    
    return summaParsed

def generateContentsHtml(contentsLines, summaPartStr):
    contentsIndices = processContentsIndices(contentsLines)
    firstQuestionIndex = [key for key, value in contentsIndices['runningQuestionTypeCategory'].items() if value == 'question'][0]
    trimmedRunningContentsIndices = {key: value for key, value in contentsIndices['runningQuestionTypeCategory'].items() if key >= firstQuestionIndex-1}

    questionsAndTitles = {}
    titleCnt = 0
    priorLineType = 'sectionTitle'
    for lineNum, lineType in trimmedRunningContentsIndices.items():
        #print(contentsLines[lineNum], lineType)
        if lineType == 'question':
            if priorLineType != 'sectionTitle':
                questionsAndTitles[questionNum] = activeQuestionTitle
            questionSearch = re.search(patterns['contentsQuestionLines'], contentsLines[lineNum])
            questionNum = int(questionSearch.group(1))
            activeQuestionTitle = questionSearch.group(2)
        elif lineType == 'continuedQuestion':
            continuedQuestionSearch = re.search(patterns['continuedContentsQuestionLine'], contentsLines[lineNum])
            activeQuestionTitle += f" {continuedQuestionSearch.group(1)}"
        elif lineType == 'sectionTitle':
            if priorLineType == 'question' or priorLineType == 'continuedQuestion':
                questionsAndTitles[questionNum] = activeQuestionTitle
            questionsAndTitles[f"title{titleCnt}"] = contentsLines[lineNum]
            titleCnt += 1
        priorLineType = lineType

    questionsAndTitles[questionNum] = activeQuestionTitle #clean up the last one

    contentsHtmlBuilder = Airium()
    with contentsHtmlBuilder.head():
        contentsHtmlBuilder.title(_t=f"Summa Theologiae {summaPartStr}: Contents")
        contentsHtmlBuilder.link(href="./../styles.css", rel="stylesheet")
        contentsHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')
    with contentsHtmlBuilder.div(id='mainwrap'):
        with contentsHtmlBuilder.div(style="text-align: center"):
            contentsHtmlBuilder.h1(_t=f"Summa Theologiae {summaPartStr}: Contents")
        for key, value in questionsAndTitles.items():
            if type(key) == int:
                contentsHtmlBuilder.a(href=f"./questions/summa{summaPartStr}q{key}.html", style="text-decoration: underline", _t=f"{key} {value}")
            else:
                contentsHtmlBuilder.br()
                contentsHtmlBuilder.br()
                with contentsHtmlBuilder.b():
                    contentsHtmlBuilder(value)
                #contentsHtmlBuilder.br()
            contentsHtmlBuilder.br()

    return contentsHtmlBuilder

def generateQuestionHtml(questionLines, summaPartStr):
    questionNum = re.search(patterns['questionStart'], questionLines[0]).group(1)
    questionTitle = f"{questionLines[2].strip()} {questionLines[3]}"
    
    questionIndices = processQuestionIndices(questionLines)

    singleArticle = questionIndices['articleSeparators'] == []

    if singleArticle:
        questionSummary = []
        articleBookends = [0] + [len(questionLines)]
        questionLines[2] = f'FIRST ARTICLE [{summaPartStr}, Q. {questionNum}, Art. 1]'
    else: 
        questionSummary = questionLines[4:questionIndices['articleSeparators'][0]]
        articleBookends = questionIndices['articleSeparators'] + [len(questionLines)]

    articlesParsed = []
    for i in range(len(articleBookends) - 1):
        articleLines = questionLines[articleBookends[i]+2:articleBookends[i+1]]
        if len(articleLines) > 5:
            articlesParsed.append(
                parseArticle(articleLines)
            )
    
    questionHtmlBuilder = Airium()
    with questionHtmlBuilder.head():
        questionHtmlBuilder.title(_t=f"Summa Theologiae {summaPartStr}, Q. {questionNum}")
        questionHtmlBuilder.link(href="./../../styles.css", rel="stylesheet")
        questionHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with questionHtmlBuilder.div(id='mainwrap'):
        with questionHtmlBuilder.div(style="text-align: center"):
            questionHtmlBuilder.h1(_t=f"QUESTION {questionNum}")
            questionHtmlBuilder.h2(_t=f"{questionTitle}")
        questionHtmlBuilder.br()

        for summaryLine in questionSummary:
            if summaryLine == '\n':
                questionHtmlBuilder.br()
            else:
                questionHtmlBuilder(summaryLine)

        questionHtmlBuilder.br()
        questionHtmlBuilder.br()

        for articleParsed in articlesParsed:
            generateArticleHtml(
                questionHtmlBuilder=questionHtmlBuilder,
                articleParsed=articleParsed
            )

    return questionHtmlBuilder

def generateArticleHtml(questionHtmlBuilder, articleParsed):
    questionHtmlBuilder.b(_t=f"{articleParsed['articleTitle']}")
    with questionHtmlBuilder.div(id='tightwrap'):
        #with questionHtmlBuilder.details(style='BACKGROUND-COLOR: #458B00; display:block;'):
        with questionHtmlBuilder.details():
            questionHtmlBuilder.summary(_t="Objections and Replies")

            with questionHtmlBuilder.div(id='expansionwrap'):
                with questionHtmlBuilder.span():

                    for objectionNum, objectionLines in articleParsed['objections'].items():
                        with questionHtmlBuilder.b():
                            with questionHtmlBuilder.i():
                                questionHtmlBuilder(f"Objection {objectionNum}:")
                        questionHtmlBuilder(" ".join(objectionLines))
                        questionHtmlBuilder.br()
                        questionHtmlBuilder.br()

                        if objectionNum in articleParsed['replies'].keys():
                            with questionHtmlBuilder.b():
                                with questionHtmlBuilder.i():
                                    questionHtmlBuilder(f"Reply Objection {objectionNum}:")
                            questionHtmlBuilder(" ".join(articleParsed['replies'][objectionNum]))
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.hr()
                            questionHtmlBuilder.br()
        
        if articleParsed['sedContra'] != [] or articleParsed['respondeo'] != []:
            with questionHtmlBuilder.details():
                questionHtmlBuilder.summary(_t="Aquinas' Arguments")
                with questionHtmlBuilder.div(id='expansionwrap'):
                    with questionHtmlBuilder.span():
                        
                        if articleParsed['sedContra'] != []:
                            with questionHtmlBuilder.b():
                                with questionHtmlBuilder.i():
                                    questionHtmlBuilder("Sed contra,")
                            questionHtmlBuilder(f"{articleParsed['sedContra'][0][19:]}")
                            if len(articleParsed['sedContra']) > 1:
                                questionHtmlBuilder(" ".join(articleParsed['sedContra'][1:]))
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.br()

                        if articleParsed['respondeo'] != []:
                            with questionHtmlBuilder.b():
                                with questionHtmlBuilder.i():
                                    questionHtmlBuilder("Respondeo,")
                            questionHtmlBuilder(f"{articleParsed['respondeo'][0][17:]}")
                            if len(articleParsed['respondeo']) > 1:
                                questionHtmlBuilder(" ".join(articleParsed['respondeo'][1:]))
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.br()

        questionHtmlBuilder.br()

def summaDriver(rawSummaTextAddress, summaPartStr, destinationDirectory):
    with open(rawSummaTextAddress, 'r', encoding='utf-8') as file:
        #lines = [x for x in file.readlines() if x != '\n']
        summaLines = file.readlines()

    if 'questions' not in os.listdir(destinationDirectory):
        os.mkdir(f"{destinationDirectory}/questions/")

    summaLines = alterSummaLines(summaLines, summaPartStr)

    summaParsed = parseSumma(summaLines)

    contentsHtml = generateContentsHtml(
        contentsLines = summaParsed['contentsLines'],
        summaPartStr = summaPartStr
    )
    with open(f"{destinationDirectory}/summa{summaPartStr}Contents.html", 'wb') as file:
        file.write(bytes(contentsHtml))

    questionNum = 1
    for questionLines in summaParsed['questionsLines']:
        #print(questionNum)
        questionHtml = generateQuestionHtml(
            questionLines=questionLines,
            summaPartStr=summaPartStr
        )
        with open(f"{destinationDirectory}/questions/summa{summaPartStr}q{questionNum}.html", 'wb') as file:
            file.write(bytes(questionHtml))

        questionNum += 1