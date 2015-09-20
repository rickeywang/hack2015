#!/usr/bin/env python

import webapp2
from google.appengine.ext import ndb
from utils import to_json
from wrappers.firebase import FirebaseWrapper
import string
import json

class MarkerHandler(webapp2.RequestHandler):
    def post(self):
        # Add a manual marker to a trip
        # So hacky cause end of hackathon and sleepy :(
        request = self.request.body
        request = string.replace(request, '[', '')
        request = string.replace(request, ']', '')
        request = string.replace(request, '"', '')
        request = request.split(',')

        count = 0

        for item in request:
            if count == 0:
                lat = item
            elif count == 1:
                long = item
            else:
                trip_id = item
            count += 1

        user = ndb.Key(urlsafe=trip_id).parent().get()
        trip = ndb.Key(urlsafe=trip_id).get()

        payload = {
            'lat' : lat,
            'long': long
        }

        request = {
            "user_id" : user.key.urlsafe(),
            "trip_id" : trip.key.urlsafe(),
            "payload" : json.dumps(payload)
        }

        fb_wrapper = FirebaseWrapper()
        fb_response = fb_wrapper.firebase_post(request)

        if fb_response.status_code != 200:
            logging.error(fb_response.content)
            self.response.status_int = 400
            self.response.headers['Access-Control-Allow-Origin'] = "http://www.myvoyagr.co"
            self.response.write("Error saving marker")
            return

        self.response.status_int = 200
        self.response.headers['Access-Control-Allow-Origin'] = "http://www.myvoyagr.co"
        self.response.write("Success")
        return

