#!/usr/bin/env python

from google.appengine.api import urlfetch
from utils import FIREBASE_URL, FIREBASE_KEY

class FirebaseWrapper:
    def post(self, request):
        firebase_result = {}

        if request.get('email') is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to post trip - Missing user email'})
            return

        if request.get('trip') is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to post trip - Missing trip id'})
            return


        qry = User.query(User.email==request.get('email')).get()
        if qry is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to post trip - User does not exist'})
            return


        # Get user's key urlsafe id
        # Get trip key urlsafe id
