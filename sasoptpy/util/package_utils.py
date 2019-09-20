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
Package-wide utility functions
"""

from collections import Iterable
import random
import string
import warnings
from contextlib import contextmanager

import sasoptpy
from sasoptpy._libs import (pd, np)


def load_package_globals():
    sasoptpy.itemid = 0

    # Constant values
    sasoptpy.MIN = 'MIN'
    sasoptpy.MAX = 'MAX'
    sasoptpy.CONT = 'CONT'
    sasoptpy.INT = 'INT'
    sasoptpy.BIN = 'BIN'
    sasoptpy.STR = 'str'
    sasoptpy.NUM = 'num'

    sasoptpy.LSO = 'lso'
    sasoptpy.MIP = 'mip'
    sasoptpy.LP = 'lp'
    sasoptpy.QP = 'qp'

    sasoptpy.N = sasoptpy.Symbol(name='_N_')

    # Container for wrapped statements
    sasoptpy._transfer = {}
    sasoptpy.transfer_allowed = False

    # Transformation dictionary
    sasoptpy._transform = {
        'binary': sasoptpy.BIN,
        'bin': sasoptpy.BIN,
        'integer': sasoptpy.INT,
        'int': sasoptpy.INT,
        'continuous': sasoptpy.CONT,
        'cont': sasoptpy.CONT,
        'maximize': sasoptpy.MAX,
        'max': sasoptpy.MAX,
        'minimize': sasoptpy.MIN,
        'min': sasoptpy.MIN,
        'string': sasoptpy.STR,
        'str': sasoptpy.STR,
        'number': sasoptpy.NUM,
        'num': sasoptpy.NUM
    }

    # Relation dictionary
    sasoptpy._relation_dict = {
        'E': '=',
        'EQ': '=',
        'NE': '!=',
        'LT': '<',
        'LE': '<=',
        'L': '<=',
        'GT': '>',
        'GE': '>=',
        'G': '>=',
        'IN': 'in'
    }


def get_creation_id():
    sasoptpy.itemid += 1
    return sasoptpy.itemid


def get_next_name():
    return 'o' + str(get_creation_id())


def is_existing_object(obj):
    if obj.get_name() is None:
        return False
    elif get_obj_by_name(obj.get_name()):
        return True
    else:
        return False


def need_name_assignment(obj, name):
    if obj.get_name() is None:
        return True
    elif obj.get_name() == name:
        return False
    else:
        return True


def set_creation_order_if_empty(obj):
    if hasattr(obj, '_objorder') and not obj._objorder:
        obj._objorder = get_creation_id()


def load_function_containers():
    sasoptpy.container = None

    def read_statement_dictionary():
        d = dict()
        d[sasoptpy.core.Model.set_objective] = \
            sasoptpy.abstract.statement.ObjectiveStatement.set_objective_of_model

        d[sasoptpy.core.Model.solve] = \
            sasoptpy.abstract.statement.SolveStatement.solve

        d[sasoptpy.core.Variable.set_bounds] = \
            sasoptpy.abstract.statement.Assignment.set_bounds

        d[sasoptpy.abstract.ParameterValue.set_value] = \
            sasoptpy.abstract.statement.Assignment.set_value

        d[sasoptpy.abstract.Parameter.set_value] = \
            sasoptpy.abstract.statement.Assignment.set_value

        d[sasoptpy.core.Model.drop_constraint] = \
            sasoptpy.abstract.statement.DropStatement.drop_constraint

        d[sasoptpy.core.util.read_data] = \
            sasoptpy.abstract.statement.ReadDataStatement.read_data

        return d

    sasoptpy.statement_dictionary = read_statement_dictionary()


def load_condition_container():
    sasoptpy.conditions = None


def load_default_mediators():
    sasoptpy.mediators['CAS'] = sasoptpy.interface.CASMediator
    sasoptpy.mediators['SAS'] = sasoptpy.interface.SASMediator


def register_to_function_container(func1, func2):
    sasoptpy.statement_dictionary[func1] = func2


def get_in_digit_format(val):
    """
    Returns a value by rounding it to config digits

    Parameters
    ----------
    val : float or integer
        Variable to be formatted into string

    Returns
    -------
    for : str
        Formatted string

    """
    digits = sasoptpy.config['max_digits']
    if digits and digits > 0:
        return round(val, digits)
    return val


def round_digits(val):
    digits = sasoptpy.config['print_digits']
    if digits and digits > 0:
        return round(val, digits)
    return val


def get_direction_str(direction):
    return sasoptpy._relation_dict.get(direction)


def _extract_argument_as_list(inp):

    if isinstance(inp, int):
        thelist = list(range(0, inp))
    elif isinstance(inp, range):
        thelist = list(inp)
    elif isinstance(inp, tuple):
        thelist = inp[0]
    elif isinstance(inp, list):
        thelist = inp
    elif sasoptpy.abstract.is_abstract_set(inp):
        thelist = [inp]
    else:
        thelist = list(inp)
    return thelist


def extract_list_value(tuplist, listname):
    """
    Extracts values inside various object types

    Parameters
    ----------
    tuplist : tuple
        Key combination to be extracted
    listname : dict or list or int or float or DataFrame or Series object
        List where the value will be extracted

    """
    if listname is None:
        v = None
    elif isinstance(listname, dict):
        v = listname[tuple_unpack(tuplist)]
    elif np.isinstance(type(listname), np.number):
        v = listname
    elif isinstance(listname, pd.DataFrame):
        if isinstance(listname.index, pd.MultiIndex):
            v = listname.loc[tuplist[:-1]][tuplist[-1]]
        else:
            v = listname.loc[tuplist]
    elif isinstance(listname, pd.Series):
        v = listname.loc[tuplist]
    else:
        v = listname
        for k in tuplist:
            v = v[k]
    return v


def is_key_abstract(key):
    import sasoptpy.abstract
    return sasoptpy.abstract.util.is_key_abstract(key)


def pack_to_tuple(obj):
    """
    Converts a given object to a tuple object

    If the object is a tuple, the function returns the input,
    otherwise creates a single dimensional tuple

    Parameters
    ----------
    obj : Object
        Object that is converted to a tuple

    Returns
    -------
    t : tuple
        Tuple that includes the original object
    """
    if isinstance(obj, tuple):
        return obj
    elif isinstance(obj, str):
        return (obj,)
    return (obj,)


def get_first_member(tp):
    """
    Grabs the first element in a tuple, if a tuple is given as argument

    Parameters
    ----------
    tp : tuple

    """
    if isinstance(tp, tuple):
        if len(tp) == 1:
            return tp[0]
    return tp


def tuple_unpack(tp):
    warnings.warn('Use sasoptpy.util.get_first_member', DeprecationWarning)
    return get_first_member(tp)


def tuple_pack(obj):
    warnings.warn('Use sasoptpy.util.pack_to_tuple', DeprecationWarning)
    return pack_to_tuple(obj)


def pack_to_list(obj):
    it = type(obj)
    if it == list:
        return obj
    else:
        return [obj]


def list_pack(obj):
    warnings.warn('Use sasoptpy.util.pack_to_list', DeprecationWarning)
    return pack_to_list(obj)


def _list_item(obj):
    warnings.warn('Use sasoptpy.util.pack_to_list', DeprecationWarning)
    return pack_to_list(obj)


def _wrap_expression_with_iterators(exp, operator, iterators):
    if isinstance(exp, sasoptpy.core.Variable):
        r = exp.copy()
    else:
        r = exp
    if r.get_name() is None:
        r.set_name(get_next_name())
    if r._operator is None:
        r._operator = operator
    for i in iterators:
        if isinstance(i, sasoptpy.abstract.SetIterator):
            r._iterkey.append(i)
    wrapper = sasoptpy.core.Expression()
    wrapper.set_member(key=r.get_name(), ref=r, val=1)
    wrapper._abstract = True
    return wrapper


def _to_optmodel_loop(keys, parent=None):
    s = ''
    subindex = []
    for key in keys:
        if isinstance(key, tuple):
            for i in flatten_tuple(key):
                subindex.append(str(i))
        elif isinstance(key, sasoptpy.abstract.SetIteratorGroup):
            subindex.append(key.get_name())
        elif not is_key_abstract(key):
            subindex.append(safe_string(str(key)))
    if subindex:
        s += '_' + '_'.join(subindex)
    iters = get_iterators(keys)
    conds = get_conditions(keys)
    if parent is not None:
        conds.extend(get_conditions(parent))
    if len(iters) > 0:
        s += ' {'
        s += ', '.join(iters)
        if len(conds) > 0:
            s += ': '
            s += ' and '.join(conds)
        s += '}'
    return s


def _recursive_walk(obj, func, attr=None, alt=None):
    """
    Calls a given method recursively for given objects


    Parameters
    ----------
    func : string
        Name of the method / function be called
    attr : string, optional
        An attribute which triggers an alternative method to be called if\
        exists
    alt : string, optional
        Name of the alternative method / function to be called if passed attr\
        exists for given objects

    Notes
    -----
    - This function is for internal consumption.

    """
    result = []
    for i in list(obj):
        if isinstance(i, list):
            result.append(recursive_walk(i, func))
        else:
            if attr is None:
                m_call = getattr(i, func)
                result.append(m_call())
            else:
                m_attr = getattr(i, attr)
                if m_attr:
                    m_call = getattr(i, alt)
                else:
                    m_call = getattr(i, func)
                result.append(m_call())
    return result


def is_set_abstract(arg):
    return sasoptpy.abstract.is_abstract_set(arg)


def is_abstract(arg):
    return hasattr(arg, '_abstract') and arg._abstract


def is_comparable(arg):
    forbidden_types = [pd.Series, pd.DataFrame, dict, tuple]
    if any(isinstance(arg, f) for f in forbidden_types):
        return False
    else:
        return True


def is_model(arg):
    return isinstance(arg, sasoptpy.core.Model)


def is_workspace(arg):
    return isinstance(arg, sasoptpy.session.Workspace)


def get_iterators(keys):
    """
    Returns a list of definition strings for a given list of SetIterators
    """
    iterators = []
    groups = {}
    for key in keys:
        if is_key_abstract(key):
            iterators.append(key._get_for_expr())
        elif isinstance(key, tuple):
            for subkey in key:
                if hasattr(subkey, '_group'):
                    g = groups.setdefault(subkey._group, [])
                    g.append(subkey)
    if groups:
        for kg in groups.values():
            s = '<' + ','.join([i.get_name() for i in kg]) + '> in ' +\
                kg[0]._set.get_name()
            iterators.append(s)
    return iterators


def get_conditions(keys):
    conditions = []
    for key in keys:
        if sasoptpy.core.util.is_expression(key):
            if key.sym.get_conditions_len() > 0:
                conditions.append(key.sym.get_conditions_str())
    return conditions


def to_condition_expression(exp):
    if hasattr(exp, '_cond_expr'):
        return exp._cond_expr()


def get_mutable(exp):
    """
    Returns a mutable copy of the given expression if it is immutable

    Parameters
    ----------
    exp : Variable or Expression
        Object to be wrapped

    Returns
    -------
    r : Expression
        Mutable copy of the expression, if the original is immutable
    """
    if isinstance(exp, sasoptpy.Variable):
        r = sasoptpy.Expression(exp)
        r._abstract = exp._abstract
    elif isinstance(exp, sasoptpy.Expression):
        r = exp
    else:
        r = sasoptpy.core.Expression(exp)
    return r


def wrap_expression(e, abstract=False):
    """
    Wraps expression inside another expression
    """
    wrapper = sasoptpy.Expression()

    if hasattr(e, 'get_name') and e.get_name() is not None:
        name = e.get_name()
    else:
        name = get_next_name()

    if sasoptpy.core.util.is_expression(e):
        wrapper.set_member(key=name, ref=e, val=1)
        wrapper._abstract = e._abstract or abstract
    elif isinstance(e, dict):
        wrapper._linCoef[name] = {**e}
    elif isinstance(e, str):
        wrapper = sasoptpy.Auxiliary(base=e)
    elif np.isinstance(type(e), np.number):
        wrapper += e

    return wrapper


def wrap(e, abstract=False):
    warnings.warn('Use sasoptpy.util.wrap_expression', DeprecationWarning)
    return wrap_expression(e, abstract)


def flatten_tuple(tp):
    """
    Flattens nested tuples

    Parameters
    ----------

    tp : tuple
        Nested tuple to be flattened

    Returns
    -------
    elem : Generator-type
        A generator-type object representing the flat tuple

    Examples
    --------
    >>> tp = (3, 4, (5, (1, 0), 2))
    >>> print(list(so.flatten_tuple(tp)))
    [3, 4, 5, 1, 0, 2]

    """
    for elem in tp:
        if isinstance(elem, tuple):
            yield from flatten_tuple(elem)
        else:
            yield elem


def _to_optmodel_expr(item):
    expr_func = getattr(item, "_expr", None)
    if callable(expr_func):
        return item._expr()
    else:
        return str(item)


def _to_optmodel_quoted_string(item):
    if isinstance(item, int):
        return str(item)
    elif isinstance(item, str):
        return "'{}'".format(item)
    elif isinstance(item, tuple):
        return '<' + ','.join(_to_optmodel_quoted_string(j) for j in item) + '>'
    else:
        return str(item)


def _to_quoted_string(item):
    warnings.warn('Use _to_optmodel_quoted_string', DeprecationWarning)
    return _to_optmodel_quoted_string(item)


def list_length(listobj):
    """
    Returns the length of an object if it is a list, tuple or dict

    Parameters
    ----------
    listobj : list, tuple or dict
        Object whose length will be returned

    Returns
    -------
    ln : int
        Length of the list, tuple or dict
    """
    if (isinstance(listobj, list) or isinstance(listobj, tuple) or
            isinstance(listobj, dict)):
        return len(listobj)
    else:
        return 1


def _sort_tuple(i):
    i = pack_to_tuple(i)
    key = (len(i),)
    for s in i:
        if isinstance(s, str):
            key += (0,)
        elif np.isinstance(type(s), np.number):
            key += (1,)
        elif isinstance(s, tuple):
            key += (2,)
    key += i
    return key


def _to_sas_string(obj):
    if hasattr(obj, '_expr'):
        return obj._expr()
    elif isinstance(obj, str):
        return "'{}'".format(obj)
    elif isinstance(obj, tuple):
        return ', '.join(_to_sas_string(i) for i in obj)
    elif isinstance(obj, list):
        return '{{{}}}'.format(','.join([_to_sas_string(i) for i in obj]))
    elif isinstance(obj, range):
        if obj.step == 1:
            return '{}..{}'.format(_to_sas_string(obj.start),
                                   _to_sas_string(obj.stop))
        else:
            return '{}..{} by {}'.format(_to_sas_string(obj.start),
                                         _to_sas_string(obj.stop),
                                         _to_sas_string(obj.step))
    elif np.isinstance(type(obj), np.number):
        return str(obj)
    else:
        raise TypeError('Cannot convert type {} to SAS string'.format(type(obj)))
        return '{}'.format(str(obj))


def _insert_brackets(prefix, keys):
    if keys is None:
        return prefix
    else:
        s = prefix + '['
        k = pack_to_tuple(keys)
        s += ', '.join(_to_iterator_expression(k))
        s += ']'
        return s


def _to_iterator_expression(itlist):
    strlist = []
    for i in itlist:
        if isinstance(i, sasoptpy.core.Expression):
            strlist.append(i._expr())
        elif isinstance(i, str):
            strlist.append("'{}'".format(i))
        else:
            strlist.append(str(i))
    return strlist


def _to_bracket(prefix, keys):
    warnings.warn('Use sasoptpy.util.package_utils._insert_brackets', DeprecationWarning)
    return _insert_brackets(prefix, keys)


def get_python_symbol(symbol):
    if symbol == '^':
        return '**'
    else:
        return symbol


def get_unsafe_operators():
    return ['+', '-', '/', '**', '^', '(', ')', 'sum']


def safe_string(st):
    return "".join(c if c.isalnum() else '_' for c in st)


def get_object_order(obj):
    return getattr(obj, '_objorder', None)


def get_attribute_definitions(members):
    definitions = [_attribute_to_defn(i) for i in members]
    defn = '\n'.join(definitions)
    return defn


def _attribute_to_defn(d):
    expr = sasoptpy.util.to_expression
    if d['key'] == 'init':
        return '{} = {};'.format(expr(d['ref']), d['value'])
    if d['key'] == 'lb' or d['key'] == 'ub':
        return '{}.{} = {};'.format(expr(d['ref']), d['key'], d['value'])
    raise NotImplementedError(
        'Attribute {} definition is not implemented'.format(d['key']))


def addSpaces(s, space):
    white = ' '*space
    return white + white.join(s.splitlines(1))


def get_session_type(sess):
    if sess is None:
        return None
    else:
        sess_type = type(sess).__name__
        if sess_type == 'CAS':
            return 'CAS'
        elif sess_type == 'SASsession':
            return 'SAS'
        else:
            return None


# def safe_variable_name(name):
#     return name.replace(' ', '_').replace('\'', '')


def get_group_name(name):
    return name.split('[')[0]


def has_expr(e):
    return hasattr(e, '_expr')


def generator_iter(parent, argv):
    with sasoptpy.inside_container(parent):
        yield enumerate(argv)