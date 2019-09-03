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
Unit tests for core classes.
"""

import os
import unittest
import sasoptpy as so
from inspect import cleandoc
from sasoptpy.actions import read_data


class TestReadData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from swat import CAS, SWATError
        try:
            cls.conn = CAS(os.environ.get('CASHOST'),
                           int(os.environ.get('CASPORT')),
                           authinfo=os.environ.get('AUTHINFO'))
        except SWATError:
            raise unittest.SkipTest('Cannot establish CAS connection. ' \
                                    + 'Check your environment variables ' \
                                    + '(CASHOST, CASPORT, AUTHINFO)')
        except TypeError:
            raise unittest.SkipTest('Environment variable may not be defined')

    def setUp(self):
        pass

    def test_read_regular_existing(self):

        from sasoptpy import Workspace, VariableGroup
        from sasoptpy.abstract import Set, ParameterGroup
        from sasoptpy.actions import solve

        with Workspace('test_workspace') as ws:

            ITEMS = Set(name='ITEMS')
            value = ParameterGroup(ITEMS, name='value', init=0)
            get = VariableGroup(ITEMS, name='get', vartype=so.INT, lb=0)

            read_data(
                table="values",
                index={'target': ITEMS, 'key': None},
                columns=[{'target': value}])

            solve(options={'with': so.LSO, 'maxgen': 10})

        optmodel_code = so.to_optmodel(ws)
        self.assertEqual(optmodel_code, cleandoc("""
            proc optmodel;
                set ITEMS;
                num value {ITEMS} init 0;
                var get {{ITEMS}} integer >= 0;
                read data values into ITEMS value;
                solve with lso / maxgen=10;
            quit;
            """))

    def test_read_data_index(self):

        with so.Workspace('test_read_data_n') as ws:
            ASSETS = so.Set(name='ASSETS')
            ret = so.ParameterGroup(ASSETS, name='return', ptype=so.NUM)
            read_data(
                table='means',
                index={'target': ASSETS, 'key': so.N},
                columns=[{'target': ret}]
            )
        optmodel_code = so.to_optmodel(ws)
        self.assertEqual(optmodel_code, cleandoc("""
            proc optmodel;
                set ASSETS;
                num return {ASSETS};
                read data means into ASSETS=[_N_] return;
            quit;
            """))

    def test_read_data_no_index_expression(self):

        from sasoptpy.util import iterate

        with so.Workspace('test_read_data_no_index_expression') as ws:
            ASSETS = so.Set(name='ASSETS')
            cov = so.ParameterGroup(ASSETS, ASSETS, name='cov', init=0)
            with iterate(ASSETS, 'asset1') as asset1, iterate(ASSETS, 'asset2') as asset2:
                read_data(
                    table='covdata',
                    index={'key': [asset1, asset2]},
                    columns=[
                        {'target': cov},
                        {'target': cov[asset2, asset1],
                         'column': 'cov'}
                    ]
                )

        optmodel_code = so.to_optmodel(ws)
        self.assertEqual(optmodel_code, cleandoc("""
            proc optmodel;
                set ASSETS;
                num cov {ASSETS, ASSETS} init 0;
                read data covdata into [asset1 asset2] cov cov[asset2, asset1]=cov;
            quit;
            """))

    def test_read_data_col(self):

        from sasoptpy.util import concat

        with so.Workspace('test_read_data_col') as ws:
            n = so.Parameter(name='n', init=2)
            indx = so.Set(name='indx', settype=['num'])
            p = so.ParameterGroup(indx, name='p')
            q = so.ParameterGroup(indx, name='q')

            read_data(
                table='exdata',
                index={
                    'target': indx,
                    'key': so.N
                },
                columns=[
                    {'target': p, 'column': 'column1'},
                    {'target': q, 'column': concat('column', n)}
                ]
            )

        optmodel_code = so.to_optmodel(ws)
        self.assertEqual(optmodel_code, cleandoc("""
            proc optmodel;
                num n init 2;
                set indx;
                num p {indx};
                num q {indx};
                read data exdata into indx=[_N_] p=column1 q=col('column' || n);
            quit;
            """))

    def test_read_data_indexed_column(self):

        from sasoptpy.util import iterate, concat

        with so.Workspace(name='test_read_data_idx_col') as ws:
            dow = so.Set(name='DOW', value=so.exp_range(1, 5))
            locs = so.Set(name='LOCS', settype=so.STR)
            demand = so.ParameterGroup(locs, dow, name='demand')

            with iterate(locs, name='loc') as loc:
                r = read_data(
                    table='dmnd',
                    index={'target': locs, 'key': loc}
                )
                with iterate(dow, name='d') as d:
                    r.append({
                        'index': d,
                        'target': demand[loc, d],
                        'column': concat('day', d)
                    })

        optmodel_code = so.to_optmodel(ws)
        self.assertEqual(optmodel_code, cleandoc("""
            proc optmodel;
                set DOW = 1..5;
                set <str> LOCS;
                num demand {LOCS, DOW};
                read data dmnd into LOCS=[loc] {d in DOW} < demand[loc, d]=col('day' || d) >;
            quit;"""))

    def test_with_cas_data(self):
        if not TestReadData.conn:
            unittest.skip('No session is available')

        from sasoptpy.util import concat
        import pandas as pd
        df = pd.DataFrame([
            [1, 2], [3, 4]
        ], columns=['column1', 'column2'])

        s = TestReadData.conn
        exdata = s.upload_frame(df, casout='exdata')

        with so.Workspace('test_read_data_col', session=s) as ws:
            n = so.Parameter(name='n', init=2)
            indx = so.Set(name='indx', settype=['num'])
            p = so.ParameterGroup(indx, name='p')
            q = so.ParameterGroup(indx, name='q')

            read_data(
                table=exdata,
                index={
                    'target': indx,
                    'key': so.N
                },
                columns=[
                    {'target': p, 'column': 'column1'},
                    {'target': q, 'column': concat('column', n)}
                ]
            )

            from sasoptpy.actions import print_item
            print_item(p, q)

        optmodel_code = so.to_optmodel(ws)
        self.assertEqual(optmodel_code, cleandoc("""
            proc optmodel;
                num n init 2;
                set indx;
                num p {indx};
                num q {indx};
                read data EXDATA into indx=[_N_] p=column1 q=col('column' || n);
                print p q;
            quit;
            """))

        response = ws.submit()
        self.assertEqual(response['Print1.PrintTable'].to_string(), cleandoc(
            """
               COL1    p    q
            0   1.0  1.0  2.0
            1   2.0  3.0  4.0
            """
        ))

    def test_read_data_no_index_target(self):

        with so.Workspace('test_no_index_target') as ws:
            NODES = so.Set(name='NODES', settype=so.STR)
            nodesByPri = so.ParameterGroup(NODES, name='nodesByPri')

            read_data(table='temppri',
                      index={'key': so.N},
                      columns=[
                          {'target': nodesByPri, 'column': 'id'}
                      ])

        self.assertEqual(so.to_optmodel(ws), cleandoc("""
            proc optmodel;
                set <str> NODES;
                num nodesByPri {NODES};
                read data temppri into [_N_] nodesByPri=id;
            quit;
            """))

    def test_read_data_same_name_cols(self):

        from sasoptpy.actions import set_objective, solve

        with so.Workspace('test_same_name_cols') as ws:
            x = so.Variable(name='x')
            y = so.Variable(name='y')
            c_xx = so.Parameter(name='c_xx')
            c_x = so.Parameter(name='c_x')
            c_y = so.Parameter(name='c_y')
            c_xy = so.Parameter(name='c_xy')
            c_yy = so.Parameter(name='c_yy')
            read_data(table='coeff',
                      index={},
                      columns=[
                          {'target': c_xx, 'column': 'c_xx'},
                          {'target': c_x},
                          {'column': 'c_y'},
                          {'target': c_xy, 'column': 'c_xy'},
                          {'target': c_yy}
                      ])
            set_objective(c_xx * x**2 + c_x * x + c_xy * x * y + c_yy * y**2,
                          name='z', sense=so.MIN)
            solve()

        self.assertEqual(so.to_optmodel(ws), cleandoc("""
            proc optmodel;
                num c_xx;
                num c_x;
                num c_y;
                num c_xy;
                num c_yy;
                read data coeff into c_xx c_x c_y c_xy c_yy;
                MIN z = c_xx * (x) ^ (2) + c_x * x + c_xy * x * y + c_yy * (y) ^ (2);
                solve;
            quit;
            """))

    def test_read_data_var_bound(self):

        from sasoptpy.util import iterate

        with so.Workspace('test_read_data_var_bound') as ws:
            plants = so.Set(name='plants', settype=so.STR)
            prod = so.VariableGroup(plants, name='prod', lb=0)
            cost = so.Parameter(name='cost', ptype=so.NUM)
            with iterate(plants, 'p') as p:
                r = read_data(
                    table='pdat',
                    index={'target': plants, 'key': p},
                    columns=[
                        {'target': prod[p].ub, 'column': 'maxprod'},
                        {'target': cost}
                    ])

        self.assertEqual(so.to_optmodel(ws), cleandoc("""
            proc optmodel;
                set <str> plants;
                var prod {{plants}} >= 0;
                num cost;
                read data pdat into plants=[p] prod[p].ub=maxprod cost;
            quit;
            """))

    def test_read_data_with_exp(self):

        with so.Workspace('test_read_data_with_exp') as ws:

            ss = so.Set(name='subscripts', value=so.exp_range(1,4), settype=so.NUM)
            letter = so.ParameterGroup(ss, name='letter', ptype=so.STR)
            read_data(
                table='abcd',
                index={'key': so.N},
                columns=[
                    {'target': letter[5-so.N]}
                ]
            )

        self.assertEqual(so.to_optmodel(ws), cleandoc("""
            proc optmodel;
                set subscripts = 1..4;
                str letter {subscripts};
                read data abcd into [_N_] letter[- _N_ + 5];
            quit;
            """))

    def test_read_data_append_later(self):

        from sasoptpy.util import concat, iterate

        with so.Workspace('let') as ws:
            actors = so.Set(name='ACTORS')
            actor_name = so.ParameterGroup(actors, ptype=so.STR,
                                           name='actor_name')
            daily_fee = so.ParameterGroup(actors, name='daily_fee')
            most_scenes = so.Parameter(name='most_scenes', value=9)
            scene_list = so.ParameterGroup(actors, so.exp_range(1, most_scenes),
                                           name='scene_list')

            r = read_data(
                table='scene',
                index={
                    'target': actors,
                    'key': so.N
                },
                columns=[
                    {
                        'target': actor_name,
                        'column': 'Actor'
                    },
                    {
                        'target': daily_fee,
                        'column': 'DailyFee'
                    }
                ]
            )
            with iterate(so.exp_range(1, most_scenes), name='j') as j:
                r.append({
                    'index': j,
                    'target': scene_list[so.N, j],
                    'column': concat('S_Var', j)
                })

        self.assertEqual(so.to_optmodel(ws), cleandoc("""
            proc optmodel;
                set ACTORS;
                str actor_name {ACTORS};
                num daily_fee {ACTORS};
                num most_scenes = 9;
                num scene_list {ACTORS, 1..most_scenes};
                read data scene into ACTORS=[_N_] actor_name=Actor daily_fee=DailyFee {j in 1..most_scenes} < scene_list[_N_, j]=col('S_Var' || j) >;
            quit;
            """))

    def test_read_data_multi_index(self):

        with so.Workspace('test_read_data_multi_index') as ws:
            arcs = so.Set(name='ARCS', settype=[so.STR, so.STR])
            arc_lower = so.ParameterGroup(arcs, name='arcLower')
            arc_upper = so.ParameterGroup(arcs, name='arcUpper')
            arc_cost = so.ParameterGroup(arcs, name='arcCost')

            read_data(
                table='arcdata',
                index={
                    'target': arcs,
                    'key': ['_tail_', '_head_']
                },
                columns=[
                    {'target': arc_lower, 'column': '_lo_'},
                    {'target': arc_upper, 'column': '_capac_'},
                    {'target': arc_cost, 'column': '_cost_'}
                ]
            )

        self.assertEqual(so.to_optmodel(ws), cleandoc("""
            proc optmodel;
                set <str, str> ARCS;
                num arcLower {ARCS};
                num arcUpper {ARCS};
                num arcCost {ARCS};
                read data arcdata into ARCS=[_tail_ _head_] arcLower=_lo_ arcUpper=_capac_ arcCost=_cost_;
            quit;
            """))

    def tearDown(self):
        pass