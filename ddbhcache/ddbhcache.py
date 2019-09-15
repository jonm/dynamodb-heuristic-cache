# Copyright (C) 2017-2019 Jonathan T. Moore
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

import datetime
import hashlib
import logging
import json
import sys
import time

import boto3
import dateutil.parser

class UTC(datetime.tzinfo):
    def utcoffset(self, dt): return datetime.timedelta(0)
    def tzname(self, dt): return 'UTC'
    def dst(self, dt): return datetime.timedelta(0)

_utc = UTC()

class Cache:
    def __init__(self, dynamodb_table_name, heuristic_freshness=0.1,
                 dynamodb=None):
        self._table_name = dynamodb_table_name
        self._heuristic_freshness = heuristic_freshness
        if dynamodb is None:
            dynamodb = boto3.resource('dynamodb')
        self._table = dynamodb.Table(self._table_name)

    def _is_fresh(self, item, now=None):
        if now is None:
            now = datetime.datetime.now(_utc)
        if 'date' not in item or 'last_modified' not in item:
            return False

        fetched = dateutil.parser.parse(item['date'])
        last_modified = dateutil.parser.parse(item['last_modified'])
        stable_for = now - last_modified
        portion = int(1.0 / self._heuristic_freshness)
        return (now - fetched) < (stable_for / portion)

    def lookup(self, key):
        item = None

        resp = self._table.get_item(Key = { 'key' : key })
        if resp is None or 'Item' not in resp:
            return None
        item = resp['Item']
        
        if self._is_fresh(item):
            try:
                return json.loads(item['body'])
            except (KeyError, ValueError) as e:
                return None
        else:
            return None

    def update(self, key, body):
        now = datetime.datetime.now(_utc)

        item = None
        resp = self._table.get_item(Key = { 'key' : key })
        if resp is not None and 'Item' in resp:
            item = resp['Item']

        if item is not None and item['body'] == body:
            item['date'] = now.isoformat()
            self._table.put_item(Item = item)
        else:
            self._table.put_item(
                Item = { 'key' : key,
                         'body' : body,
                         'date' : now.isoformat(),
                         'last_modified' : now.isoformat() })

