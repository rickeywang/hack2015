#!/usr/bin/env python

import webapp2
from handlers.user import UserHandler
from handlers.trip import TripHandler
from handlers.marker import MarkerHandler

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write({'response': "Hello, World!  You're on a page we haven't built yet, come back again soon!"})

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/user', UserHandler),
    ('/user/(.*)', UserHandler),
    ('/trip', TripHandler),
    ('/trip/(.*)', TripHandler),
    ('/marker', MarkerHandler)
], debug=True)

