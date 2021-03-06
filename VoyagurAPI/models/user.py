#!/usr/bin/env python

from google.appengine.ext import ndb
import time

class User(ndb.Model):
    email = ndb.StringProperty(indexed=True)            # Email of the user
    created = ndb.DateTimeProperty(auto_now_add=True)   # User account creation

    def format(self):
        return {
            'id' : self.key.urlsafe(),
            'created' : time.mktime(self.created.timetuple())
        }
