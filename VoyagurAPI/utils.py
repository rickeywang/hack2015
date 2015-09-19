#!/usr/bin/env python

import ast
import string

# Change a string into a dict
def to_json(request):
    # Ensure that all 'true's and 'false'es are replaced with their Python equivalents before
    # parsing. Will cause a Malformed String error otherwise.
    # Super hacky. I know.
    request = string.replace(request, 'true', 'True')
    request = string.replace(request, 'false', 'False')

    return ast.literal_eval(request)
