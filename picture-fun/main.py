#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# inject './lib' dir in the path so that we can simply do "import ndb"
# or whatever there's in the app lib dir.
import sys

if 'lib' not in sys.path:
    sys.path[0:0] = ['lib']

import webapp2
import urllib
import json
import logging
import base64

from google.appengine.api import urlfetch
from google.appengine.api import images


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class get_img_handler(webapp2.RedirectHandler):
    def get(self):
        # input params
        img_url = "https://storage.googleapis.com/htn_user_photos/rickey_test/2015-04-30%2008.11.49.jpg"
        # get from google drive API files.get
        img_description = "Last day in Mountain View. Love these guys! Gonna miss them sigh..."

        # api config
        # indico
        indico_t1api_url = "http://apiv2.indico.io/keywords"
        indico_t2api_url = "http://apiv2.indico.io/namedentities"
        indico_i1api_url = "http://apiv2.indico.io/faciallocalization"
        indico_i2api_url = "http://apiv2.indico.io/fer"
        indico_api_key = 'fea9a6fc90bc7df59d5e7f108d87620a'
        indico_params = {
            "key": indico_api_key
        }
        indico_txt_payload = {
            'data': img_description,
        }
        # ms azure
        az_cvapi_url = "https://api.projectoxford.ai/vision/v1/analyses"
        az_api_key = "cb503783adc3467f82b1fb5e48103d0d"
        az_cvapi_headers = {
            'Content-Type' : 'application/json', # we will ask azure to grab the image itself, prob faster
            'Ocp-Apim-Subscription-Key': az_api_key
        }


        #indico text
        indico_param_data = urllib.urlencode(indico_params)
        indico_response = urlfetch.fetch(method=urlfetch.POST, url=indico_t1api_url + "?" + indico_param_data, payload=json.dumps(indico_txt_payload))
        self.response.write(indico_response.content)
        indico_response = urlfetch.fetch(method=urlfetch.POST, url=indico_t2api_url + "?" + indico_param_data, payload=json.dumps(indico_txt_payload))
        self.response.write(indico_response.content)

        #indico emotion
        #get img file and convert to base64
        img_request_response = urlfetch.fetch(method=urlfetch.GET, url=img_url)
        img_bin_data = img_request_response.content
        az_cvapi_payload = json.dumps({
            "Url":img_url
        })
        #self.response.write(indico_img_payload)
        #send img to az for face coordinates
        az_response = urlfetch.fetch(method=urlfetch.POST,
                                     url=az_cvapi_url,
                                     payload=az_cvapi_payload,
                                     headers=az_cvapi_headers)
        az_cvapi_response = json.loads(az_response.content)
        self.response.write(az_cvapi_response)
        #crop each one
        for i in range(len(az_cvapi_response['faces'])):
            img_manip_obj = images.Image(img_bin_data)
            #self.response.write(img_face_coord)
            x1 = float(az_cvapi_response['faces'][i]['faceRectangle']['left'])
            y1 = float(az_cvapi_response['faces'][i]['faceRectangle']['top'])
            w = float(az_cvapi_response['faces'][i]['faceRectangle']['width'])
            h = float(az_cvapi_response['faces'][i]['faceRectangle']['height'])
            img_manip_obj.crop(x1/img_manip_obj.width,
                               y1/img_manip_obj.height,
                               (x1+w)/img_manip_obj.width,
                               (y1+h)/img_manip_obj.height
                               )
            faces_bin_data = img_manip_obj.execute_transforms(output_encoding=images.JPEG)
            self.response.write('<img src=\"data:image/jpeg;base64,' + base64.b64encode(faces_bin_data)+'\"/>')
            #get emotion of the face
            indico_img_payload = {
                'data': base64.b64encode(faces_bin_data)
            }
            indico_response = urlfetch.fetch(method=urlfetch.POST,
                                             url=indico_i2api_url + "?" + indico_param_data,
                                             payload=json.dumps(indico_img_payload))
            img_face_emo = json.loads(indico_response.content)
            self.response.write(img_face_emo)


        cv_api_url = "http://api.imagga.com/v1/tagging"
        cv_params = {
                        "url": img_url,
                        "version": "2"
                        }
        cv_headers = {
                    'accept': "application/json",
                    'authorization': "Basic YWNjX2YyOWY4M2M1MTk1ZjFiNzozOTRkOTM0NWY2NzUzODY0MzlkNTc2ZWRmNDI1YzFmYw=="
                    }

        cv_param_data = urllib.urlencode(cv_params)

        #cv_response = urlfetch.fetch(method=urlfetch.GET, url=cv_api_url + "?" + param_data, headers=headers)

        # convert to base64 and store

        # debug show
        #self.response.write(response.content)


        # save that to firebase entity of the image

        # some pretty display thing for the tags




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/get_img', get_img_handler)
], debug=True)
