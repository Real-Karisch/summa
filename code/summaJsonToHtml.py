from airium import Airium
import json
import os
import re

from variables import patterns, summaParts
from htmlFormats import formatStrToHtml

def generateQuestionHtml(questionJson, summaPartStr):    
    questionHtmlBuilder = Airium()
    with questionHtmlBuilder.head():
        questionHtmlBuilder.title(_t=f"Summa Theologiae {summaPartStr}, Q. {questionJson['questionNum']}")
        questionHtmlBuilder.link(href="./../../styles.css", rel="stylesheet")
        questionHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with questionHtmlBuilder.div(id='mainwrap'):
        with questionHtmlBuilder.div(style="text-align: center"):
            questionHtmlBuilder.h1(_t=f"QUESTION {questionJson['questionNum']}")
            questionHtmlBuilder.h2(_t=f"{questionJson['questionTitle']}")
        questionHtmlBuilder.br()

        questionHtmlBuilder(
            formatStrToHtml(questionJson['questionSummary'])
        )

        questionHtmlBuilder.br()
        questionHtmlBuilder.br()

        for articleJson in questionJson['articles']:
            #print(articleJson['articleNum'])
            generateArticleHtml(
                questionHtmlBuilder=questionHtmlBuilder,
                articleJson=articleJson
            )

    return questionHtmlBuilder

def generateArticleHtml(questionHtmlBuilder, articleJson):
    questionHtmlBuilder.b(_t=f"{articleJson['articleTitle']}")
    with questionHtmlBuilder.div(id='tightwrap'):
        #with questionHtmlBuilder.details(style='BACKGROUND-COLOR: #458B00; display:block;'):
        with questionHtmlBuilder.details():
            questionHtmlBuilder.summary(_t="Objections and Replies")

            with questionHtmlBuilder.div(id='expansionwrap'):
                with questionHtmlBuilder.span():

                    for objectionJson in articleJson['objections']:
                        with questionHtmlBuilder.b():
                            with questionHtmlBuilder.i():
                                questionHtmlBuilder(f"Objection {objectionJson['objectionNum']}:")
                        questionHtmlBuilder(
                            formatStrToHtml(objectionJson['objectionField'])
                        )
                        questionHtmlBuilder.br()
                        questionHtmlBuilder.br()

                        replyList = [x for x in articleJson['replies'] if x['replyNum'] == objectionJson['objectionNum']]
                        if replyList != []:
                            replyJson = replyList[0]
                            with questionHtmlBuilder.b():
                                with questionHtmlBuilder.i():
                                    questionHtmlBuilder(f"Reply Objection {replyJson['replyNum']}:")
                            questionHtmlBuilder(
                                formatStrToHtml(replyJson['replyField'])
                            )
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.hr()
                            questionHtmlBuilder.br()
        
        if articleJson['sedContraField'] != '' or articleJson['respondeoField'] != '':
            with questionHtmlBuilder.details():
                questionHtmlBuilder.summary(_t="Aquinas' Arguments")
                with questionHtmlBuilder.div(id='expansionwrap'):
                    with questionHtmlBuilder.span():
                        
                        if articleJson['sedContraField'] != '':
                            with questionHtmlBuilder.b():
                                with questionHtmlBuilder.i():
                                    questionHtmlBuilder("Sed contra,")
                            questionHtmlBuilder(
                                formatStrToHtml(f"{articleJson['sedContraField'][19:]}")
                            )
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.br()

                        if articleJson['respondeoField'] != '':
                            with questionHtmlBuilder.b():
                                with questionHtmlBuilder.i():
                                    questionHtmlBuilder("Respondeo,")
                            questionHtmlBuilder(
                                formatStrToHtml(f"{articleJson['respondeoField'][17:]}")
                            )
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.br()

        questionHtmlBuilder.br()

def generateContentsHtml(contentsJson, summaPartStr):
    contentsHtmlBuilder = Airium()
    with contentsHtmlBuilder.head():
        contentsHtmlBuilder.title(_t=f"Summa Theologiae {summaPartStr}: Contents")
        contentsHtmlBuilder.link(href="./../styles.css", rel="stylesheet")
        contentsHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with contentsHtmlBuilder.div(id='mainwrap'):
        with contentsHtmlBuilder.div(style="text-align: center"):
            contentsHtmlBuilder.h1(_t=f"Summa Theologiae {summaPartStr}: Contents")
        for sectionJson in contentsJson:
            contentsHtmlBuilder.br()
            contentsHtmlBuilder.br()
            contentsHtmlBuilder.br()
            with contentsHtmlBuilder.b():
                contentsHtmlBuilder(sectionJson['sectionTitle'])
            for questionTitle in sectionJson['sectionQuestions']:
                questionNumber = re.search(patterns['contentsQuestionLines'], questionTitle).group(1)
                contentsHtmlBuilder.br()
                contentsHtmlBuilder.a(href=f"./questions/summa{summaPartStr}q{questionNumber}.html", style="text-decoration: underline", _t=questionTitle)
    return contentsHtmlBuilder

def generateAllSummasHtml(allSummasJson, htmlDestinationFolder):
    for summaJson in allSummasJson:
        summaPartNum = summaJson['partNum']
        if summaParts[summaPartNum]['camelName'] not in os.listdir(htmlDestinationFolder):
            os.mkdir(f"{htmlDestinationFolder}/{summaParts[summaPartNum]['camelName']}")
        if 'questions' not in os.listdir(f"{htmlDestinationFolder}/{summaParts[summaPartNum]['camelName']}"):
            os.mkdir(f"{htmlDestinationFolder}/{summaParts[summaPartNum]['camelName']}/questions")

        contentsHtml = generateContentsHtml(
            contentsJson=summaJson['contents'],
            summaPartStr=summaParts[summaPartNum]['str']
        )

        with open(f"{htmlDestinationFolder}/{summaParts[summaPartNum]['camelName']}/summa{summaParts[summaPartNum]['str']}Contents.html", 'wb') as file:
            file.write(bytes(contentsHtml))

        for questionJson in summaJson['questions']:
            questionHtml = generateQuestionHtml(
                questionJson=questionJson,
                summaPartStr=summaParts[summaPartNum]['str']
            )

            with open(f"{htmlDestinationFolder}/{summaParts[summaPartNum]['camelName']}/questions/summa{summaParts[summaPartNum]['str']}q{questionJson['questionNum']}.html", 'wb') as file:
                file.write(bytes(questionHtml))

if __name__ == '__main__':
    with open('C:/Users/jackk/Projects/summa/json/allSummas.json', 'r') as file:
        allSummasJson = json.load(file)

    generateAllSummasHtml(
        allSummasJson=allSummasJson,
        htmlDestinationFolder='C:/Users/jackk/Projects/summa/html/summa/'
    )