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

"""
Test for symbolic conditions
"""

import os
import sys
import unittest
import warnings
import sasoptpy as so
from inspect import cleandoc

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
from util import assert_equal_wo_temps

class TestCondition(unittest.TestCase):

    def test_regular_condition(self):

        from sasoptpy.util import iterate
        from sasoptpy.actions import condition

        x = so.VariableGroup(3, name='x')
        c = so.ConstraintGroup(None, name='c')
        with iterate([1, 2, 3], 's') as i:
            with condition(i != 2):
                c[i] = x[i] <= 3

        print(so.to_definition(c))

    def test_container_condition(self):

        from sasoptpy.util import iterate
        from sasoptpy.actions import condition, set_objective, solve, expand

        with so.Workspace(name='w') as w:

            x = so.VariableGroup(3, name='x')
            # solve
            x[0].set_value(1)
            x[1].set_value(5)
            x[2].set_value(0)

            c = so.ConstraintGroup(None, name='c')

            with iterate([0, 1, 2], 's') as i:
                with condition(x[i].sym > 0):
                    c[i] = x[i] >= 1

            set_objective(x[0], name='obj', sense=so.MIN)
            expand()
            solve()

        assert_equal_wo_temps(self, so.to_optmodel(w), cleandoc(
            '''
            proc optmodel;
                var x {{0,1,2}};
                x[0] = 1;
                x[1] = 5;
                x[2] = 0;
                con c {s in {0,1,2}: x[s].sol > 0} : x[s] >= 1;
                MIN obj = x[0];
                expand;
                solve;
            quit;'''
        ))

    def test_nested_conditions(self):

        from sasoptpy.actions import condition

        S = so.Set(name='S')
        P = so.Set(name='P')
        x = so.VariableGroup(S, name='x')
        c = so.ConstraintGroup(None, name='c')
        d = so.ConstraintGroup(None, name='d')
        e = so.ConstraintGroup(None, name='e')
        for i in S:
            with condition(2 * i <= 5):
                t = i * x[i] <= 5
                c[i] = t
                with condition(i**2 >= 3):
                    d[i] = x[i] - i >= 5
                with condition((i >= 4) | (i <= 2)):
                    e[i] = x[i] >= 0

        assert_equal_wo_temps(
            self, so.to_definition(c),
            'con c {o9 in S: 2.0 * o9 <= 5} : o9 * x[o9] <= 5;')

        assert_equal_wo_temps(
            self, so.to_definition(d),
            'con d {o9 in S: 2.0 * o9 <= 5 and (o9) ^ (2) >= 3} : x[o9] - o9 >= 5;')

        assert_equal_wo_temps(
            self, so.to_definition(e),
            'con e {o9 in S: 2.0 * o9 <= 5 and ((o9 >= 4) or (o9 <= 2))} : x[o9] >= 0;')
