
from collections import OrderedDict
from types import GeneratorType

import sasoptpy
import sasoptpy.abstract
from .util import (is_parameter)
from sasoptpy.core.util import (is_expression)


class ExpressionDict:
    """
    Creates a dictionary of :class:`Expression` objects

    Parameters
    ----------
    name : string
        Name of the object

    Examples
    --------

    >>> e[0] = x + 2*y
    >>> e[1] = 2*x + y**2
    >>> print(e.get_keys())
    >>> for i in e:
    >>>     print(i, e[i])
    (0,) x + 2 * y
    (1,) 2 * x + (y) ** (2)


    Notes
    -----
    - ExpressionDict is the underlying class for :class:`ImplicitVar`.
    - It behaves as a regular dictionary for client-side models.
    """

    def __init__(self, name=None):
        name = sasoptpy.util.assign_name(name, 'impvar')
        self._name = name
        self._objorder = sasoptpy.util.register_globally(name, self)
        self._dict = OrderedDict()
        self._conditions = []
        self._shadows = OrderedDict()
        self._abstract = False

    def __setitem__(self, key, value):
        key = sasoptpy.util.pack_to_tuple(key)

        # Set name for named types
        ntypes = [sasoptpy.abstract.Parameter, sasoptpy.core.Expression]
        if any(isinstance(value, i) for i in ntypes) and value._name is None:
            value._name = self._name

        # Add the dictionary value
        if is_parameter(value):
            self._dict[key] = sasoptpy.abstract.ParameterValue(value, key)
        elif is_expression(value):
            self._dict[key] = value
            if value._abstract:
                self._abstract = True
        else:
            self._dict[key] = value

    def __getitem__(self, key):
        key = sasoptpy.util.pack_to_tuple(key)
        if key in self._dict:
            return self._dict[key]
        elif key in self._shadows:
            return self._shadows[key]
        else:
            if self._abstract and len(self._dict) <= 1:
                tuple_key = sasoptpy.util.pack_to_tuple(key)
                pv = sasoptpy.abstract.ParameterValue(self, tuple_key)
                self._shadows[key] = pv
                return pv
            else:
                return None

    def _defn(self):
        # Do not return a definition if it is a local dictionary
        s = ''
        if len(self._dict) == 1:
            s = 'impvar {} '.format(self._name)
            if ('',) not in self._dict:
                s += '{'
                key = self._get_only_key()
                s += ', '.join([i._defn() for i in list(key)])
                s += '} = '
            else:
                key = self._get_only_key()
                s += '= '
            item = self._dict[key]
            if isinstance(item, sasoptpy.abstract.ParameterValue):
                s += self._dict[key]._ref._expr()
            else:
                s += self._dict[key]._expr()
            s += ';'
        #======================================================================
        # else:
        #     s = ''
        #     for key, val in self._dict.items():
        #         ref = self._name + sasoptpy.util._to_optmodel_loop(key)
        #         s += 'impvar {}'.format(ref)
        #         s += ' = ' + (val._expr()
        #                       if hasattr(val, '_expr') else str(val)) + ';\n'
        #======================================================================
        return s

    def get_keys(self):
        """
        Returns the dictionary keys

        Returns
        -------
        d : dict_keys
            Dictionary keys stored in the object
        """
        return self._dict.keys()

    def __iter__(self):
        return self._dict.__iter__()

    def _get_only_key(self):
        return list(self._dict.keys())[0]

    def __str__(self):
        return self._name

    def __repr__(self):
        s = 'sasoptpy.ExpressionDict(name=\'{}\', '.format(self._name)
        if len(self._dict) == 1:
            key = self._get_only_key()
            s += 'expr=('
            try:
                s += self._dict[key]._ref._expr()
            except AttributeError:
                s += str(self._dict[key])
            if ('',) not in self._dict:
                s += ' ' + ' '.join(['for ' + i._defn() for i in list(key)])
            s += ')'
        s += ')'
        return s


class ImplicitVar(ExpressionDict):
    """
    Creates an implicit variable

    Parameters
    ----------
    argv : Generator, optional
        Generator object for the implicit variable
    name : string, optional
        Name of the implicit variable

    Notes
    -----

    - If the loop inside generator is over an abstract object, a definition
      for the object will be created inside :meth:`Model.to_optmodel` method.

    Examples
    --------

    Regular Implicit Variable

    >>> I = range(5)
    >>> x = so.Variable(name='x')
    >>> y = so.VariableGroup(I, name='y')
    >>> z = so.ImplicitVar((x + i * y[i] for i in I), name='z')
    >>> for i in z:
    >>>     print(i, z[i])
    (0,) x
    (1,) x + y[1]
    (2,) x + 2 * y[2]
    (3,) x + 3 * y[3]
    (4,) x + 4 * y[4]

    Abstract Implicit Variable

    >>> I = so.Set(name='I')
    >>> x = so.Variable(name='x')
    >>> y = so.VariableGroup(I, name='y')
    >>> z = so.ImplicitVar((x + i * y[i] for i in I), name='z')
    >>> print(z._defn())
    impvar z {i_1 in I} = x + i_1 * y[i_1];
    >>> for i in z:
    >>>     print(i, z[i])
    (sasoptpy.abstract.SetIterator(name=i_1, ...),) x + i_1 * y[i_1]

    """

    def __init__(self, argv=None, name=None):
        super().__init__(name=name)
        if argv:
            if type(argv) == GeneratorType:
                for arg in argv:
                    keynames = ()
                    keyrefs = ()
                    if argv.gi_code.co_nlocals == 1:
                        itlist = argv.gi_code.co_cellvars
                    else:
                        itlist = argv.gi_code.co_varnames
                    localdict = argv.gi_frame.f_locals
                    for i in itlist:
                        if i != '.0':
                            keynames += (i,)
                    for i in keynames:
                        keyrefs += (localdict[i],)
                    self[keyrefs] = arg
            elif (type(argv) == sasoptpy.expression.Expression and
                  argv._abstract):
                self[''] = argv
                self['']._objorder = self._objorder
            elif type(argv) == sasoptpy.expression.Expression:
                self[''] = argv
                self['']._objorder = self._objorder
            else:
                print('ERROR: Unrecognized type for ImplicitVar argument: {}'.
                      format(type(argv)))