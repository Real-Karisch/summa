The workflow takes the raw Project Gutenberg txt files of the summa, one text file for each part, then makes a single json containing each part of the summa as a separate element of a list. The functions to run this part of the program can be found in summaToJson.py.

Structure of the allSummas json:

    summas list(dict):
        partNum: int
        contents: list(dict):
            sectionTitle: str
            sectionQuestions: list(str)
        questions list(dict):
            questionNum: int
            questionTitle: str
            questionSummary: str
            articles: list(dict)
                articleNum: int
                articleTitle: str
                objections: list(dict)
                    objectionNum: int
                    objectionField: str
                replies: list(dict)
                    replyNum: int
                    replyField: str
                sedContraField: str
                respondeoField: str

Then the json is converted into a full summa html site pointed at a folder of the user's choice. This folder just needs to contain a styles.css file for formatting as well as an index html file to serve as the master directory to send the user into whichever part he selects. The functions to run this part can be found in summaJsonToHtml.py.

Finally, supporting dicts used during each part of the process are in variables.py, and supporting text processing/managing functions are found in utils.py.