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

Then the json is converted into a full summa html site pointed at a folder of the user's choice. This folder just needs to contain a styles.css file for formatting. The functions to run this part can be found in summaJsonToHtml.py.

During conversion of json to html, the strings that make up the objections, replies, and body of the articles run through a converter to apply html formatting. The functions that make up this converter can be found in htmlFormats.py.

These are the rules that are used for the html conversion:
    htmlSingleTagTranslations: these patterns are replaced by a single html tag (i.e. not an opening AND closing tag), e.g. <br>
        '  ' (double space): <br>

    htmlRegionTagTranslations: these patterns are replaced by an opening and closing tag, e.g. <i></i>. Obviously this means that the symbol has to appear as a pair in the string; these replacements also can include a dynamicAttribute, the value of which will be whatever appears after "#" and before the second symbol in the pair in the string (e.g. "This is an @example#Here is a note.@ string." becomes "This is an <span title="Here is a note.">example</span> string.")
        _: <i></i>
        @: <span title=""></span>

Supporting dicts used during each part of the process are in variables.py, and supporting text processing/managing functions are found in utils.py.

All html edits to the objection, reply and body strings can be made in the allSummas.json files, which will then be converted into html. The allSummas_raw.json file WILL BE overwritten by the summaToJson.py file so any edits there will be discarded.