#!/usr/bin/env python

import webapp2

from google.appengine.api import urlfetch
from utils import to_json

from models.user import User

class UserHandler(webapp2.RequestHandler):
    """
    POST /user

    Create a user given a Google token
    """
    def post(self):
        request = to_json(self.request.body)

        # Verify the token on the Google servers
        url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={}".format(request.get('token'))
        result = urlfetch.fetch(url=url,
            method=urlfetch.GET,
        )

        if result.get('status_code') == 200:
            content = result.get('body')
            # Need to check the 'aud' property once we have a user to actually test this stuff with.
            # For now we'll just assume everything worked and return a formatted new user

            qry = User.query(User.email==content.get('email')).get()

            if qry is None:
                # Need to create a new user
                user = User()
                user.email = content.get('email')
                user.put()
