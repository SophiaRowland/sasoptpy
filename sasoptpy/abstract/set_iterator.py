
from collections import OrderedDict
import sasoptpy
from .condition import Conditional


class SetIterator(sasoptpy.Expression):
    """
    Creates an iterator object for a given Set

    Parameters
    ----------
    initset : Set
        Set to be iterated on
    name : string, optional
        Name of the iterator
    datatype : string, optional
        Type of the iterator

    Notes
    -----

    - SetIterator objects are automatically created when looping over a
      :class:`Set`.
    - This class is mainly intended for internal use.
    - The ``group`` parameter consists of following keys

      - **order** : int
        Order of the parameter inside the group
      - **outof** : int
        Total number of indices inside the group
      - **id** : int
        ID number assigned to group by Python

    """

    def __init__(self, initset, name=None, datatype=None):
        if name is None:
            name = sasoptpy.util.get_next_name()
        super().__init__(name=name)
        self.set_member(key=name, ref=self, val=1.0)
        self._set = initset
        if datatype is None:
            datatype = sasoptpy.NUM
        self._type = datatype
        self.sym = Conditional(self)

    def get_type(self):
        return self._type

    def __hash__(self):
        return hash('{}'.format(id(self)))

    def _get_for_expr(self):
        return '{} in {}'.format(self._expr(),
                                 sasoptpy.to_expression(self._set))

    def _expr(self):
        return self.get_name()

    def __str__(self):
        return self._name

    def _defn(self):
        return self._get_for_expr()

    def __repr__(self):
        s = 'sasoptpy.SetIterator({}, name=\'{}\')'.format(self._set, self.get_name())
        return s


class SetIteratorGroup(OrderedDict):

    def __init__(self, initset, datatype=None, names=None):
        super()
        self._name = sasoptpy.util.get_next_name()
        self._set = initset
        self._init_members(names, datatype)

    def _init_members(self, names, datatype):
        if names is not None:
            for i, name in enumerate(names):
                dt = datatype[i] if datatype is not None else None
                it = SetIterator(None, name=name, datatype=dt)
                self.append(it)
        else:
            for i in datatype:
                it = SetIterator(None, datatype=i)
                self.append(it)

    def get_name(self):
        return self._name

    def append(self, object):
        name = object.get_name()
        self[name] = object

    def _get_for_expr(self):
        #return '<{}> in {}'.format(self._expr(), self._set._name)
        comb = '<' + ', '.join(str(i) for i in self.values()) + '>'
        s = '{} in {}'.format(comb, sasoptpy.to_expression(self._set))
        return s

    def _expr(self):
        return ', '.join(str(i) for i in self.values())

    def _defn(self):
        return self._get_for_expr()


    def __iter__(self):
        for i in self.values():
            yield i

    def __repr__(self):
        return 'sasoptpy.SetIteratorGroup({}, datatype=[{}], names=[{}])'.format(
            self._set,
            ', '.join('\'' + i.get_type() + '\'' for i in self.values()),
            ', '.join('\'' + i.get_name() + '\'' for i in self.values())
        )

    def __str__(self):
        s = ', '.join(str(i) for i in self.values())
        return '(' + s + ')'

    def __hash__(self):
        hashstr = ','.join(str(id(i)) for i in self.values())
        return hash(hashstr)
