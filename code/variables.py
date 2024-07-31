summaParts = {
    1: {
        'snakeName': 'prima_pars',
        'camelName': 'primaPars',
        'str': 'I'
    },
    2: {
        'snakeName': 'prima_secundae',
        'camelName': 'primaSecundae',
        'str': 'I-II'
    },
    3: {
        'snakeName': 'secunda_secundae',
        'camelName': 'secundaSecundae',
        'str': 'II-II'
    },
    4: {
        'snakeName': 'tertia_pars',
        'camelName': 'tertiaPars',
        'str': 'III'
    },
}

patterns = {
    'questionStart': '^QUESTION (\d+)$',
    'lineSeparator': '^_+$',
    'articleFirstLine': '(\d+)\]$',
    'objectionStart': '^(Objection|Obj\.) (\d+): (.*)$',
    'replyStart': '^Reply Obj\. (\d+): (.*)$',
    'sedContraStart': '^_On the contrary',
    'respondeoStart': '^_I answer that', 
    'contentsQuestionLines': "^(\d+)\. +(.+)$",
    'emptyLines': '\n',
    'allCaps': """^[A-Z:;,./'" ]+$""",
    'continuedContentsQuestionLine': '^       (.*)$',
    'lastLine': '^\*\*\* END OF THE PROJECT GUTENBERG', 
}

hardCodeLineAlterations = {
    'I': {
        'insertions': [ #make sure these are in reverse index order to avoid pushing the later ones
            {
                'index': 52540,
                'value': 'QUESTION 116'
            },
            {
                'index': 131,
                'value': 'TREATISE ON THE ONE GOD'
            },
            {
                'index': 130,
                'value': 'TREATISE ON SACRED DOCTRINE'
            },
        ],
        'overwrites': [],
        'substitutions': [],
        'deleteRanges': [],
    },
    'I-II': {
        'insertions': [ #make sure these are in reverse index order to avoid pushing the later ones
            {
                'index': 264,
                'value': 'QUESTION 1'
            },
            {
                'index': 237,
                'value': 'TREATISE ON GRACE'
            },
            {
                'index': 194,
                'value': 'TREATISE ON VICE AND SIN'
            },
            {
                'index': 142,
                'value': 'TREATISE ON THE PASSIONS'
            },
            {
                'index': 125,
                'value': "TREATISE ON HUMAN ACTS"
            },
            {
                'index': 120,
                'value': "TREATISE ON MAN'S LAST END"
            },
        ],
        'overwrites': [
            {
                'index': 10825,
                'value': 'FIRST ARTICLE [I-II, Q. 23, Art. 1]'
            }
        ],
        'substitutions': [],
        'deleteRanges': [],
    },
    'II-II': {
        'insertions': [ #make sure these are in reverse index order to avoid pushing the later ones
            {
                'index': 73018,
                'value': 'QUESTION 183'
            },
            {
                'index': 273,
                'value': 'TREATISE ON TEMPERANCE'
            },
            {
                'index': 184,
                'value': 'TREATISE ON JUSTICE'
            },
            {
                'index': 147,
                'value': 'TREATISE ON CHARITY'
            },
            {
                'index': 141,
                'value': 'TREATISE ON HOPE'
            },
            {
                'index': 125,
                'value': 'TREATISE ON FAITH'
            },
        ],
        'overwrites': [
            {
                'index': 172,
                'value': 'TREATISE ON PRUDENCE'
            },
            {
                'index': 253,
                'value': 'TREATISE ON FORTITUDE'
            },
            {
                'index': 10894,
                'value': 'SIXTH ARTICLE [II-II, Q. 24, Art. 6]'
            },
            {
                'index': 22303,
                'value': 'FIRST ARTICLE [II-II, Q. 48, Art. 1]'
            },
            {
                'index': 34210,
                'value': 'FIRST ARTICLE [II-II, Q. 80, Art. 1]'
            },
            {
                'index': 52938,
                'value': 'FIRST ARTICLE [II-II, Q. 80, Art. 1]'
            },
            {
                'index': 57343,
                'value': 'FIRST ARTICLE [II-II, Q. 143, Art. 1]'
            },
        ],
        'substitutions': [
            {
                'index': 68615,
                'matchStr': 'Obj\. 2',
                'replaceStr': 'Reply Obj. 2'
            },
        ],
        'deleteRanges': [],
    },
    'III': {
        'insertions': [
            {
                'index': 211,
                'value': 'TREATISE ON PENANCE'
            },
            {
                'index': 200,
                'value': 'TREATISE ON THE HOLY EUCHARIST'
            },
            {
                'index': 199,
                'value': 'TREATISE ON CONFIRMATION'
            },
            {
                'index': 193,
                'value': 'TREATISE ON BAPTISM'
            },
            {
                'index': 187,
                'value': 'TREATISE ON THE SACRAMENTS'
            },
            {
                'index': 153,
                'value': 'TREATISE ON THE LIFE OF CHRIST'
            },
            {
                'index': 125,
                'value': 'TREATISE ON THE INCARNATION'
            },
        ],
        'overwrites': [],
        'substitutions': [],
        'deleteRanges': [
            {
                'indexStart': 13053,
                'indexEnd': 13178
            }
        ]
    }
}