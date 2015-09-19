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

        user = User.query(User.email==request.get('email')).get()
        trip = ndb.Key(urlsafe=request.get('trip_id')).get()

        if user is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to post trip - User does not exist'})
            return

        # Get user's key urlsafe id
        # Get trip key urlsafe id
