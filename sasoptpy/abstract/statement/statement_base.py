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

from abc import ABC, abstractmethod
from collections import OrderedDict

import sasoptpy


class Statement(ABC):

    def __init__(self):
        import sasoptpy.util
        self.parent = None
        self.header = OrderedDict()
        self.elements = list()
        self.workspace = dict()
        self._objorder = sasoptpy.util.get_creation_id()
        # TODO Remove '_after' after arranging data/structrues py files
        self._after = False

    @abstractmethod
    def _defn(self):
        pass

    def _expr(self):
        pass

    @abstractmethod
    def append(self, arg, **kwargs):
        pass