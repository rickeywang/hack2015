#!/usr/bin/env python

from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty(indexed=True)        # Email of the user
