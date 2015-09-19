#!/usr/bin/env python

from google.appengine.api import urlfetch
from utils import FIREBASE_URL, FIREBASE_KEY

from models.user import User
from models.trip import Trip

class FirebaseWrapper:
    def post(self, request):
        firebase_result = {}

        if request.get('email') is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to post trip - Missing user email'})
            return

        if request.get('trip_id') is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to post trip - Missing trip id'})
            return

        firebase_url = FIREBASE_URL
        url = firebase_url + request.get('user_id')  + "/" + request.get('trip_id') + ".json"
        payload = to_json(request.get('payload'))
        firebase_result = urlfetch.fetch(
            url,
            method = urlfetch.POST,
            payload = payload,
            headers = {
                "Content-Type"  :"application/json",
                "Authorization" : "OAuth " + FIREBASE_KEY
            }
        )

        return firebase_result
