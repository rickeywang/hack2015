#!/usr/bin/env python

from google.appengine.ext import ndb

class Trip(ndb.Model):
    start_date = ndb.DateTimeProperty(auto_now_add=True)  # Can be manually entered by the user when the Trip is being created
    start_location = ndb.GeoPtProperty() # The starting location of the trip. Can be manually entered
    end_date = ndb.DateTimeProperty()    # The end date of the trip
    end_location = ndb.GeoPtProperty()   # The last location of the trip. Can be manually entered
    name = ndb.StringProperty()          # Name of the trip

    def format(self):
        return {
            'id' : self.key.urlsafe(),
            'start_date' : self.start_date,
            'start_location' : self.start_location,
            'end_date' : self.end_date,
            'end_location' : self.end_location,
            'name'         : self.name
        }
