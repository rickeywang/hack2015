#!/usr/bin/env python

import webapp2

from google.appengine.api import urlfetch
from utils import to_json
from models.trip import Trip
from models.user import User

class TripHandler(webapp2.RequestHandler):
    def get(self, trip_id):
        if trip_id is None:
            self.response.status_int = 400
            self.response.write({'error': 'Unable to retrieve trip - Missing trip id'})
            return

        trip = Trip.get_by_id(trip_id)
        self.response.status_int = 200
        self.response.write(trip.format())
        return

    def post(self):
        """
        POST /trip

        Creates an empty Trip for the user
        """
        request = to_json(self.request.body)

        if request.get('name') is None:
            self.response.status_int = 400
            self.response.write({'error' : 'Missing name of trip'})
            return
        elif request.get('email') is None:
            self.response.status_int = 400
            self.response.write('error' : 'Missing email that the trip will be associated with')
            return
        else:
            # Check that user model exists
            user = User.query(User.email==request.get('email')).get()
            if user is None:
                self.response.status_int = 400
                self.response.write({'error' : 'Error retrieving user'})
                return

            # Create a trip with that user model as ancestor
            trip = Trip(ancestor=user.key)
            trip.put()

            self.response.status_int = 200
            self.response.write(trip.format())
            return

