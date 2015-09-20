#!/usr/bin/env python

import ast
import string

FIREBASE_URL = "https://voyagur.firebaseio.com/"
FIREBASE_KEY = "CfqHEFTEVUQWYLS5uRaOYqBgYbNT3FVTcptnsAV2"

# Change a string into a dict
def to_json(request):
    # Ensure that all 'true's and 'false'es are replaced with their Python equivalents before
    # parsing. Will cause a Malformed String error otherwise.
    # Super hacky. I know.
    request = string.replace(request, 'true', 'True')
    request = string.replace(request, 'false', 'False')

    return ast.literal_eval(request)
