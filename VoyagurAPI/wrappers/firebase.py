#!/usr/bin/env python

from google.appengine.api import urlfetch
from utils import FIREBASE_URL, FIREBASE_KEY

from models.user import User
from models.trip import Trip

class FirebaseWrapper:
    def firebase_post(self, request):
        print "IM IN FIREBASE"
        firebase_result = {}

        if request.get('user_id') is None:
            self.response.status_int = 400
            self.response.headers['Access-Control-Allow-Origin'] = "http://www.myvoyagr.co"
            self.response.write({'error': 'Unable to post trip - Missing user id'})
            return

        if request.get('trip_id') is None:
            self.response.status_int = 400
            self.response.headers['Access-Control-Allow-Origin'] = "http://www.myvoyagr.co"
            self.response.write({'error': 'Unable to post trip - Missing trip id'})
            return

        url = FIREBASE_URL + request.get('user_id')  + "/" + request.get('trip_id') + ".json"
        payload = request.get('payload')
        firebase_result = urlfetch.fetch(
            url,
            method = urlfetch.POST,
            payload = payload,
            headers = {
                "Content-Type"  :"application/json",
                "Authorization" : "OAuth {}".format(FIREBASE_KEY)
            }
        )
        return firebase_result
