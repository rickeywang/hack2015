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
import random
import string
import sys
from google.appengine.api.urlfetch_errors import DeadlineExceededError
import tagapi

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

class get_img_handler(webapp2.RequestHandler):
    img_tags = []

    def id_generator(self, size, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def add_tag(self, tag_name, weight):
        # Make sure weight is a number
        weight = float(weight)
        tag_name = tag_name.lower()

        # Check if the tag already exists
        try:
            index = [x['tag'] for x in self.img_tags].index(tag_name)
        except ValueError:
            index = -1

        # Accumulate if exists, else add it
        if index != -1:
            self.img_tags[index]['weight'] = weight + self.img_tags[index]['weight']
        else:
            self.img_tags.append({'tag': tag_name,
                                  'weight': weight})

    def get(self):
        self.img_tags = []
        # input params
        img_description = ""
        user_id = "aa"
        try:
            img_url = str(self.request.get('img_url'))
            img_file_id = self.request.get('img_id')

        except (TypeError, ValueError):
            self.response.write("<html><body><p>Invalid inputs</p></body></html>")
            img_url = "https://storage.googleapis.com/htn_user_photos/rickey_test/2015-01-25%2012.11.55.jpg"

            img_file_id = "Afaca3fa4332i8a98jiuncueaa3awefa43wra43r"
            user_id = "aa"

        # get from google drive API files.get
        img_metadata = {
            "width": 2300,
            "height": 1702,
            "date": "2015:09:20 00:06:45",
            "cameraMake": "LGE",
            "cameraModel": "Nexus 5",
            "exposureTime": 0.00029411764,
            "aperture": 2.4,
            "flashUsed": False,
            "focalLength": 3.97,
            "isoSpeed": 100,
            "meteringMode": "CenterWeightedAverage",
            "sensor": "One-chip color area",
            "exposureMode": "Auto",
            "colorSpace": "sRGB",
            "maxApertureValue": 2.53,
            "subjectDistance": 0
        }

        self.response.write('Source Image ' + img_url)
        self.response.write('<p></p>')

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
            'Content-Type': 'application/json',  # we will ask azure to grab the image itself, prob faster
            'Ocp-Apim-Subscription-Key': az_api_key
        }
        # google maps
        gmaps_rgapi_url = "https://maps.googleapis.com/maps/api/geocode/json"
        gmaps_rgapi_key = "AIzaSyDYAvQ48GMuhEMh3AZouxFRTyNeiXneZfQ"


        # indico text
        indico_param_data = urllib.urlencode(indico_params)
        indico_response = urlfetch.fetch(method=urlfetch.POST, url=indico_t1api_url + "?" + indico_param_data,
                                         payload=json.dumps(indico_txt_payload))
        indico_t1_response = json.loads(indico_response.content)
        self.response.write(indico_t1_response)
        try:
            for i in indico_t1_response['results'].keys():
                self.add_tag(i, indico_t1_response['results'][i])
        except KeyError:
            self.response.write(' Nothing for this response ')
        except TypeError:
            pass

        indico_response = urlfetch.fetch(method=urlfetch.POST, url=indico_t2api_url + "?" + indico_param_data,
                                         payload=json.dumps(indico_txt_payload))
        indico_t2_response = json.loads(indico_response.content)
        self.response.write(indico_t2_response)
        try:
            for i in indico_t2_response['results'].keys():
                self.add_tag(i, indico_t2_response['results'][i])
        except KeyError:
            self.response.write(' Nothing for indico_t2_response ')
        except TypeError:
            pass
        # indico emotion
        # get img file and convert to base64
        img_request_response = urlfetch.fetch(method=urlfetch.GET, url=img_url)
        img_bin_data = img_request_response.content
        az_cvapi_payload = json.dumps({
            "Url": img_url
        })
        # self.response.write(indico_img_payload)
        # send img to az for face coordinates
        try:
            az_response = urlfetch.fetch(method=urlfetch.POST,
                                     url=az_cvapi_url,
                                     payload=az_cvapi_payload,
                                     headers=az_cvapi_headers)
            az_cvapi_response = json.loads(az_response.content)
        except DeadlineExceededError:
            az_cvapi_response = []
        self.response.write(az_cvapi_response)
        # add azure categories
        try:
            for i in range(len(az_cvapi_response['categories'])):
                category_name = az_cvapi_response['categories'][i]['name']
                category_name = category_name.replace('_', ' ')
                self.add_tag(category_name, az_cvapi_response['categories'][i]['score'])
        except KeyError:
            self.response.write(' Nothing for this response ')

        # crop each one for emotion analysis
        try:
            for i in range(len(az_cvapi_response['faces'])):
                img_manip_obj = images.Image(img_bin_data)
                # self.response.write(img_face_coord)
                x1 = float(az_cvapi_response['faces'][i]['faceRectangle']['left'])
                y1 = float(az_cvapi_response['faces'][i]['faceRectangle']['top'])
                w = float(az_cvapi_response['faces'][i]['faceRectangle']['width'])
                h = float(az_cvapi_response['faces'][i]['faceRectangle']['height'])
                img_manip_obj.crop(x1 / img_manip_obj.width,
                                   y1 / img_manip_obj.height,
                                   (x1 + w) / img_manip_obj.width,
                                   (y1 + h) / img_manip_obj.height
                                   )
                faces_bin_data = img_manip_obj.execute_transforms(output_encoding=images.JPEG)
                self.response.write('<img src=\"data:image/jpeg;base64,' + base64.b64encode(faces_bin_data) + '\"/>')
                # get emotion of the face
                indico_img_payload = {
                    'data': base64.b64encode(faces_bin_data)
                }
                indico_response = urlfetch.fetch(method=urlfetch.POST,
                                                 url=indico_i2api_url + "?" + indico_param_data,
                                                 payload=json.dumps(indico_img_payload))
                img_face_emo = json.loads(indico_response.content)
                self.response.write(img_face_emo)

                for i in img_face_emo['results'].keys():
                    if img_face_emo['results'][i] > 0.35:
                        self.add_tag(i, img_face_emo['results'][i] / len(az_cvapi_response['faces']))

        except KeyError:
            self.response.write(' Nothing for this response ')

        # image tagging imagga
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
        cv_response_raw = urlfetch.fetch(method=urlfetch.GET, url=cv_api_url + "?" + cv_param_data, headers=cv_headers)
        cv_response = json.loads(cv_response_raw.content)
        # debug show
        self.response.write(cv_response)
        # add imagga tags
        try:
            i = 0
            while (i < 5):
                if cv_response['results'][0]['tags'][1]['confidence'] > 19:
                    self.add_tag(cv_response['results'][0]['tags'][1]['tag'],
                                 cv_response['results'][0]['tags'][1]['confidence'] / 100)
                i = i + 1
        except KeyError:
            self.response.write(' Nothing for cv_response ')
        except IndexError:
            pass

        # Reverse geocoding
        try:
            gmaps_rgapi_params = {
                'latlng': str(img_metadata['location']['latitude']) + "," + str(img_metadata['location']['longitude']),
                'key': gmaps_rgapi_key
            }
            gmaps_param_data = urllib.urlencode(gmaps_rgapi_params)
            gmaps_response = urlfetch.fetch(method=urlfetch.GET, url=gmaps_rgapi_url + "?" + gmaps_param_data)
            gmaps_rgapi_response = json.loads(gmaps_response.content)
            self.response.write(gmaps_rgapi_response)

            for i in range(len(gmaps_rgapi_response['results'][0]['address_components'])):
                for j in range(len(gmaps_rgapi_response['results'][0]['address_components'][i]['types'])):
                    if gmaps_rgapi_response['results'][0]['address_components'][i]['types'][j] == 'political' \
                            or gmaps_rgapi_response['results'][0]['address_components'][i]['types'][j] == 'route':
                        # Save this tag
                        self.add_tag(gmaps_rgapi_response['results'][0]['address_components'][i]['long_name'], 1)
        except KeyError:
            self.response.write(' Nothing for this gmap response ')



        # save that to firebase entity of the image

        # some pretty display thing for the tags

        self.response.write('<p>' + str(self.img_tags) + '</p>')

        # save the img_tags object to Firebase



        # Finally, update the Azure search index
        # BEGIN boilterplate azure code
        # First, delete all tags associated with this image
        az_searchapi1_url = "https://voyagr.search.windows.net/indexes/photos/docs"
        az_searchapi_key = 'AFA6F2086D67DDBEFEFDEDA9DD6C1D0D'
        searchapi_headers = {
            'api-key': az_searchapi_key,
            'Content-Type': "application/json; charset=utf-8"
        }
        searchapi_params = {
            "api-version": "2015-02-28",
            "$filter": "file_id eq \'" + img_file_id + "\'"
        }
        searchapi_param_data = urllib.urlencode(searchapi_params)
        searchapi_response_raw = urlfetch.fetch(method=urlfetch.GET,
                                                url=az_searchapi1_url + "?" + searchapi_param_data,
                                                headers=searchapi_headers)
        searchapi_response = json.loads(searchapi_response_raw.content)
        # debug show
        self.response.write('<p>' + str(searchapi_response) + '</p>')

        # delete the old entries. upload new entries.
        az_searchapi2_url = "https://voyagr.search.windows.net/indexes/photos/docs/index"
        search_index = {'value': []}
        try:
            # delete existing
            for i in range(len(searchapi_response['value'])):
                search_index['value'].append({
                    "@search.action": "delete",
                    "search_id": searchapi_response['value'][i]['search_id']
                })
            # add tags
            for i in range(len(self.img_tags)):
                search_index['value'].append({
                    "@search.action": "upload",
                    "search_id": self.id_generator(31),
                    "file_id": img_file_id,
                    "tag": self.img_tags[i]['tag'],
                    "user_id": user_id
                })
            # add description
            search_index['value'].append({
                "@search.action": "upload",
                "search_id": self.id_generator(31),
                "file_id": img_file_id,
                "full_text": img_description,
                "user_id": user_id
            })
        except KeyError:
            self.response.write(" azure search return was bad ")
        searchapi_params = {
            "api-version": "2015-02-28"
        }
        searchapi_param_data = urllib.urlencode(searchapi_params)
        self.response.write('<p>' + str(search_index) + '</p>')
        searchapi_response_raw = urlfetch.fetch(method=urlfetch.POST,
                                                url=az_searchapi2_url + "?" + searchapi_param_data,
                                                headers=searchapi_headers,
                                                payload=json.dumps(search_index))
        self.response.write('<p>' + str(searchapi_response_raw.content) + '</p>')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/get_img', get_img_handler),
    ('/tagapi', tagapi.tagapi)
], debug=True)
