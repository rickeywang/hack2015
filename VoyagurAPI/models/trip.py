#!/usr/bin/env python

from google.appengine.ext import ndb

class Trip(ndb.Model):
    start_date = ndb.DateTimeProperty()  # Manually entered by the user when the Trip is being created
    start_location = ndb.GeoPtProperty() # The starting location of the trip. Can be manually entered
    end_date = ndb.DateTimeProperty()    # The end date of the trip
    end_location = ndb.GeoPtProperty()   # The last location of the trip. Can be manually entered

