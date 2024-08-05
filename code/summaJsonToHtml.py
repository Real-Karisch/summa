from airium import Airium
import json
import os
import re
from string import capwords

from variables import patterns, summaParts
from htmlFormats import htmlTranslator

def generateQuestionHtml(questionJson, summaPartStr):    
    questionHtmlBuilder = Airium()
    with questionHtmlBuilder.head():
        questionHtmlBuilder.title(_t=f"Summa Theologiae {summaPartStr}, Q. {questionJson['questionNum']}")
        questionHtmlBuilder.link(href="./../../styles.css", rel="stylesheet")
        questionHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with questionHtmlBuilder.div(id='mainwrap'):
        with questionHtmlBuilder.div(style="text-align: center"):
            questionHtmlBuilder.h1(_t=f"QUESTION {questionJson['questionNum']}")
            questionHtmlBuilder.h2(_t=htmlTranslator(questionJson['questionTitle']))
        questionHtmlBuilder.br()

        questionHtmlBuilder(
            htmlTranslator(questionJson['questionSummary'])
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
    questionHtmlBuilder.b(_t=htmlTranslator(articleJson['articleTitle']))
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
                            htmlTranslator(objectionJson['objectionField'])
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
                                htmlTranslator(replyJson['replyField'])
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
                                htmlTranslator(f"{articleJson['sedContraField'][19:]}")
                            )
                            questionHtmlBuilder.br()
                            questionHtmlBuilder.br()

                        if articleJson['respondeoField'] != '':
                            with questionHtmlBuilder.b():
                                with questionHtmlBuilder.i():
                                    questionHtmlBuilder("Respondeo,")
                            questionHtmlBuilder(
                                htmlTranslator(f"{articleJson['respondeoField'][17:]}")
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
    indexHtml = generateSummaIndexHtml(allSummasJson)
    with open(f"{htmlDestinationFolder}/summa.html", 'wb') as file:
        file.write(bytes(indexHtml))

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

        with open(f"{htmlDestinationFolder}/{summaParts[summaPartNum]['camelName']}/contents.html", 'wb') as file:
            file.write(bytes(contentsHtml))

        for questionJson in summaJson['questions']:
            questionHtml = generateQuestionHtml(
                questionJson=questionJson,
                summaPartStr=summaParts[summaPartNum]['str']
            )

            with open(f"{htmlDestinationFolder}/{summaParts[summaPartNum]['camelName']}/questions/summa{summaParts[summaPartNum]['str']}q{questionJson['questionNum']}.html", 'wb') as file:
                file.write(bytes(questionHtml))

def generateSummaIndexHtml(allSummasJson):
    indexHtmlBuilder = Airium()
    with indexHtmlBuilder.head():
        indexHtmlBuilder.title(_t=f"Summa Theologiae")
        indexHtmlBuilder.link(href="styles.css", rel="stylesheet")
        indexHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')
    
    with indexHtmlBuilder.div(id='mainwrap'):
        with indexHtmlBuilder.div(style="text-align: center"):
            indexHtmlBuilder.h1(_t=f"Summa Theologiae")
            indexHtmlBuilder.br()
            indexHtmlBuilder.br()
            indexHtmlBuilder.br()

            for summaJson in allSummasJson:
                summaPartStr = summaParts[summaJson['partNum']]['str']
                summaPartFullName = summaParts[summaJson['partNum']]['fullName']
                summaPartCamelName = summaParts[summaJson['partNum']]['camelName']
                with indexHtmlBuilder.b():
                    indexHtmlBuilder.a(href=f"./{summaPartCamelName}/contents.html", style="text-decoration: underline", _t=f"{summaPartStr}: {summaPartFullName}")
                indexHtmlBuilder.br()
                for section in summaJson['contents']:
                    indexHtmlBuilder(capwords(section['sectionTitle']))
                    indexHtmlBuilder.br()
                indexHtmlBuilder.br()
                indexHtmlBuilder.br()
    
    return indexHtmlBuilder

if __name__ == '__main__':
    with open('C:/Users/jackk/Projects/summa/json/allSummas_dev.json', 'r') as file:
        allSummasJson = json.load(file)

    generateAllSummasHtml(
        allSummasJson=allSummasJson,
        htmlDestinationFolder='C:/Users/jackk/Projects/summa/html/summa/'
    )