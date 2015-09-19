#!/usr/bin/env python

import webapp2

from google.appengine.api import urlfetch
from utils import to_json
from models.trip import Trip

class TripHandler(webapp2.RequestHandler):
    def get(self, trip_id):
        if trip_id is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to retrieve trip - Missing trip id'})
            return
