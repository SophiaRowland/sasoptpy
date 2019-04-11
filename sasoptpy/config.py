#!/usr/bin/env python
# encoding: utf-8
#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import sasoptpy as so


class Config:
    """
    Option manager for sasoptpy
    """

    def __init__(self, *args):
        self.defaults = _get_default_config()
        self.overriden = dict()

        if len(args) > 1 and len(args) % 2 != 1:
            keys = args[::2]
            values = args[1::2]
            self.overriden = dict(zip(keys, values))

    def __getitem__(self, key):
        if key in self.overriden:
            return self.overriden[key]
        return self.defaults.get(key, None)

    def __setitem__(self, key, value):
        self.overriden[key] = value

    def __delitem__(self, key):
        if key in self.overriden:
            del self.overriden[key]
        else:
            raise KeyError('Invalid config key: {}'.format(key))

    def keys(self):
        dicts = [self.defaults, self.overriden]
        merged_keys = set().union(*dicts)
        return list(merged_keys)

    def __iter__(self):
        for key in self.keys():
            yield key


def _get_default_config():
    config = dict()
    config['number_format'] = '{}'
    config['max_digits'] = 12
    config['valid_outcomes'] = ['OPTIMAL', 'ABSFCONV', 'BEST_FEASIBLE']
    config['default_sense'] = so.MIN

    return config
