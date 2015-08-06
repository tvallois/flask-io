# Copyright 2015 Vinicius Chiele. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import request
from inspect import isclass
from werkzeug.http import HTTP_STATUS_CODES
from .errors import Error


def get_best_match_for_content_type(mimetypes):
    content_type = request.headers['content-type']

    mimetype_expected = content_type.split(';')[0].lower()
    for mimetype in mimetypes:
        if mimetype_expected == mimetype:
            return mimetype
    return None


def get_func_name(func):
    return func.__module__ + "." + func.__name__


def http_status_message(code):
    return HTTP_STATUS_CODES.get(code, '')


def new_if_isclass(value):
    return value() if isclass(value) else value


def unpack(value):
    data, status, headers = value + (None,) * (3 - len(value))
    return data, status, headers


def convert_marshmallow_errors(errors):
    items = []

    for field, error in errors.items():
        if isinstance(error, dict):
            for item in convert_marshmallow_errors(error):
                items.append(item)
            continue

        if isinstance(error, list):
            error = error[0]

        if isinstance(error, str):
            items.append(Error(None, error, None, field))

    return items
