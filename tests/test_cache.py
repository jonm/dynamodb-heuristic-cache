#!/usr/bin/env python
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
import unittest

from ddbhcache.ddbhcache import Cache, _utc

class DummyTable:
    def __init__(self):
        self.table_status = object()

class DummyDynamoDb:
    def __init__(self, table):
        self._table = table

    def Table(self, _):
        return self._table

class TestCache(unittest.TestCase):
    def setUp(self):
        self._table = DummyTable()
        self._ddb = DummyDynamoDb(self._table)
        self.impl = Cache('foo', dynamodb=self._ddb)

    def test_stable_item_is_fresh(self):
        now = datetime.datetime.now(_utc)
        one_day_ago = now - datetime.timedelta(days=1)
        twenty_days_ago = now - datetime.timedelta(days=20)
        item = { 'date' : one_day_ago.isoformat(),
                 'last_modified' : twenty_days_ago.isoformat() }
        self.assertTrue(self.impl._is_fresh(item, now=now))

    def test_recent_item_is_not_fresh(self):
        now = datetime.datetime.now(_utc)
        one_day_ago = now - datetime.timedelta(days=1)
        two_days_ago = now - datetime.timedelta(days=2)
        item = { 'date' : one_day_ago.isoformat(),
                 'last_modified' : two_days_ago.isoformat() }
        self.assertFalse(self.impl._is_fresh(item, now=now))

    def test_can_modify_heuristic(self):
        now = datetime.datetime.now(_utc)
        one_day_ago = now - datetime.timedelta(days=1)
        five_days_ago = now - datetime.timedelta(days=5)
        item = { 'date' : one_day_ago.isoformat(),
                 'last_modified' : five_days_ago.isoformat() }
        impl = Cache('foo', heuristic_freshness=0.33,
                     dynamodb=self._ddb)
        self.assertTrue(impl._is_fresh(item, now=now))
        

if __name__ == "__main__":
    unittest.main()
