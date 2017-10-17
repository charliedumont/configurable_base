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
from jinja2.runtime import TemplateNotFound
import webapp2
from webapp2 import WSGIApplication, Route
from webapp2_extras import jinja2

from google.appengine.ext import vendor
# Add any libraries installed in the "lib" folder.
vendor.add('lib')


# Map URLs to handlers
routes = [
    # Core API endpoints
    Route('/api/signup', handler='pbi.user.SignUp'),
    Route('/api/signup/', handler='pbi.user.SignUp'),
    Route('/api/login', handler='pbi.user.Login'),
    Route('/api/login/', handler='pbi.user.Login')
]


# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': 'SESSION_KEY'
  },
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': []
  }
}
app = WSGIApplication(routes, config=app_config, debug=True)
