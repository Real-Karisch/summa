import re
from utils import alterSummaLines, processQuestionIndices, processArticleIndices, processContentsIndices
from variables import patterns, summaParts

def listToStr(lst):
    return " ".join(
        [x.strip() for x in lst]
    ).strip()

def generateAllSummasJson(summaRawTextFolder):
    allSummasJson = []
    for summaPartNum in summaParts.keys():
        with open(f"{summaRawTextFolder}/st_raw_{summaParts[summaPartNum]['snakeName']}.txt", 'r', encoding='utf-8') as file:
            rawSummaLines = file.readlines()

        summaLines = alterSummaLines(rawSummaLines, summaParts[summaPartNum]['str'])

        allSummasJson.append(
            generateSummaJson(
                summaLines=summaLines,
                summaPartNum=summaPartNum
            )
        )

    return allSummasJson

def generateSummaJson(summaLines, summaPartNum):
    cnt = 0
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

    questions = []
    for i in range(len(questionBookends)-1):
        #parseQuestions
        questionLines = summaLines[questionBookends[i]:questionBookends[i+1]-2]
        questions.append(
            generateQuestionJson(
                questionLines=questionLines,
                summaPartStr=summaParts[summaPartNum]['str']
            )
        )

    contentsLines = summaLines[lineSeparators[2]+2:lineSeparators[3]]

    contents = generateContentsJson(contentsLines)

    return {
        'partNum': summaPartNum,
        'contents': contents,
        'questions': questions
    }


def generateQuestionJson(questionLines, summaPartStr):
    questionNum = re.search(patterns['questionStart'], questionLines[0]).group(1)
    questionTitle = f"{questionLines[2].strip()} {questionLines[3].strip()}"

    questionIndices = processQuestionIndices(questionLines)

    singleArticle = questionIndices['articleSeparators'] == []

    if singleArticle:
        questionSummary = ""
        articleBookends = [0] + [len(questionLines)]
        questionLines[2] = f'FIRST ARTICLE [{summaPartStr}, Q. {questionNum}, Art. 1]'
    else: 
        questionSummary = listToStr(questionLines[4:questionIndices['articleSeparators'][0]])
        articleBookends = questionIndices['articleSeparators'] + [len(questionLines)]

    articles = []
    for i in range(len(articleBookends) - 1):
        articleLines = questionLines[articleBookends[i]+2:articleBookends[i+1]]
        if len(articleLines) > 5:
            #parseArticles
            articles.append(
                generateArticleJson(articleLines)
            )

    return {
        'questionNum': int(questionNum),
        'questionTitle': questionTitle,
        'questionSummary': questionSummary,
        'articles': articles
    }

def generateArticleJson(articleLines):
    #print(articleLines[0])
    articleIndices = processArticleIndices(articleLines)

    articleNum = int(re.search(patterns['articleFirstLine'], articleLines[0]).group(1))

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

    objections = []
    objectionIndices = articleIndices['objectionStarts'] + [objectionEnd]
    for i in range(len(articleIndices['objectionStarts'])):
        objectionLines = articleLines[objectionIndices[i]:objectionIndices[i+1]]
        objections.append(
            generateObjectionJson(objectionLines)
        )

    replies = []
    replyIndices = articleIndices['replyStarts'] + [len(articleLines)]
    for i in range(len(articleIndices['replyStarts'])):
        replyLines = articleLines[replyIndices[i]:replyIndices[i+1]]
        replies.append(
            generateReplyJson(replyLines)
        )

    if noSedContra:
        sedContraLines = []
    else:
        if noRespondeo:
            if noReplies:
                sedContraLines = articleLines[articleIndices['sedContraStart']:]
            else:
                sedContraLines = articleLines[articleIndices['sedContraStart']:articleIndices['replyStarts'][0]]
        else:
            sedContraLines = articleLines[articleIndices['sedContraStart']:articleIndices['respondeoStart']]
    sedContraField = listToStr(sedContraLines)

    if noRespondeo:
        respondeoLines = []
    else:
        if noReplies:
            respondeoLines = articleLines[articleIndices['respondeoStart']:]
        else:
            respondeoLines = articleLines[articleIndices['respondeoStart']:articleIndices['replyStarts'][0]]
    respondeoField = listToStr(respondeoLines)

    articleTitle = f"{articleLines[0].strip()}: {listToStr(articleLines[1:articleIndices['objectionStarts'][0]])}"

    return {
        'articleNum': articleNum,
        'articleTitle': articleTitle,
        'objections': objections,
        'replies': replies,
        'sedContraField': sedContraField,
        'respondeoField': respondeoField
    }

def generateObjectionJson(objectionLines):
    objectionFirstLineSearch = re.search(patterns['objectionStart'], objectionLines[0])
    objectionNum = int(objectionFirstLineSearch.group(2))
    objectionFirstLineText = objectionFirstLineSearch.group(3)
    objectionLines[0] = objectionFirstLineText
    return {
        'objectionNum': objectionNum,
        'objectionField': listToStr(objectionLines)
    }

def generateReplyJson(replyLines):
    replyFirstLineSearch = re.search(patterns['replyStart'], replyLines[0])
    replyNum = int(replyFirstLineSearch.group(1))
    replyFirstLineText = replyFirstLineSearch.group(2)
    replyLines[0] = replyFirstLineText
    return {
        'replyNum': replyNum,
        'replyField': listToStr(replyLines)
    }

def generateContentsJson(contentsLines):
    contentsIndices = processContentsIndices(contentsLines)
    firstQuestionIndex = [key for key, value in contentsIndices['runningQuestionTypeCategory'].items() if value == 'question'][0]
    trimmedRunningContentsIndices = {key: value for key, value in contentsIndices['runningQuestionTypeCategory'].items() if key >= firstQuestionIndex-1}
    contents = []
    for index, category in trimmedRunningContentsIndices.items():
        if category == 'sectionTitle':
            contents.append(
                {
                    'sectionTitle': contentsLines[index],
                    'sectionQuestions': []
                }
            )
        elif category == 'question':
            contents[-1]['sectionQuestions'].append(contentsLines[index].strip())
        elif category == 'continuedQuestion':
            contents[-1]['sectionQuestions'][-1] += contentsLines[index].strip()

    return contents

if __name__ == '__main__':
    import json

    allSummasJson = generateAllSummasJson('C:/Users/jackk/Projects/summa/summaTxts/')

    with open(f"C:/Users/jackk/Projects/summa/json/allSummas_raw.json", 'w') as file:
        json.dump(allSummasJson, file)