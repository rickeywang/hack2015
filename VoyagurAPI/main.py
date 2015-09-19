#!/usr/bin/env python

import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write({'response': 'Hello, World!'})


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)

