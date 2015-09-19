#!/usr/bin/env python

import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from utils import to_json
from models.user import User
from models.trip import Trip

class UserHandler(webapp2.RequestHandler):
    def get(self, user_id):
        if user_id is None:
            self.response.status_int = 400
            self.response.write({'error': 'Missing user id'})
            return

        user = ndb.Key(urlsafe=user_id).get()

        if user is None:
            self.response.status_int = 400
            self.response.write({'error': 'No user exists with that ID'})
            return

        # Get all the trips associated with the user and add it to the response
        trips = {}
        trip_qry = Trip.query(ancestor=user.key).fetch()
        for trip in trip_qry:
            trips[trip.name] = trip.key.urlsafe()
        self.response.status_int = 200
        self.response.headers['Access-Control-Allow-Origin'] = "https://www.myvoyagur.co"
        self.response.write({'user': user.format(), 'trips' : trips})
        return

    """
    POST /user

    Create a user given a Google token

    Sample request body:
    {
        "token" : "1234abc"
    }
    """
    def post(self):
        request = to_json(self.request.body)

        # Verify the token on the Google servers
        # url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={}".format(request.get('token'))
        # result = urlfetch.fetch(url=url,
        #     method=urlfetch.GET,
        # )

        # if result.get('status_code') == 200:
            # content = result.get('body')
            # Need to check the 'aud' property once we have a user to actually test this stuff with.
            # For now we'll just assume everything worked and return a formatted new user

        user = User.query(User.email==request.get('email')).get()

        if user is None:
            # Need to create a new user
            user = User()
            user.email = request.get('email')
            user.put()

            self.response.status_int = 200
            self.response.headers['Access-Control-Allow-Origin'] = "https://www.myvoyagur.co"
            self.response.write(user.format())
        else:
            # Get all the trips associated with the user and add it to the response
            trips = {}
            trip_qry = Trip.query(ancestor=user.key).fetch()
            for trip in trip_qry:
                trips[trip.name] = trip.key.id()
            self.response.status_int = 200
            self.response.headers['Access-Control-Allow-Origin'] = "https://www.myvoyagur.co"
            self.response.write({'user': user.format(), 'trips' : trips})
            return

        # else:
        #     self.response.status_int = 400
        #     self.response.write({'error': 'There was an error authenticating the user'})
        #     return
