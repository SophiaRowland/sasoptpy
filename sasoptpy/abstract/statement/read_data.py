
from .statement_base import Statement
import sasoptpy


class ReadDataStatement(Statement):

    def __init__(self, table, index, columns=None):
        super().__init__()
        self._table = table
        self._index = index
        self._columns = list()
        if columns:
            for col in columns:
                self.append(col)

    def append(self, element, **kwargs):
        self._columns.append(element)

    def get_table_expr(self):
        if hasattr(self._table, 'name'):
            return self._table.name
        else:
            return str(self._table)

    def get_index_expr(self):
        index = self._index
        target = index.get('target')
        key = index.get('key')

        s = ''
        if target:
            s += '{}'.format(index['target'])
        if target and key:
            s += '='
        if key:
            s += '[{}]'.format(
                ReadDataStatement.flatten_column(key))
        return s

    def get_columns_expr(self):
        cols = self._columns
        columns_string = [ReadDataStatement.get_column_str(c) for c in cols]
        s = ' '.join(columns_string)
        return s

    @classmethod
    def flatten_column(cls, col):
        if isinstance(col, list):
            ind = [ReadDataStatement.flatten_column(c) for c in col]
            return ' '.join(ind)
        elif isinstance(col, str):
            return col
        else:
            return str(col)

    @classmethod
    def get_column_str(cls, c):
        target = c.get('target')
        column = c.get('column')
        index = c.get('index')
        target_str = ''
        connect_str = ''
        column_str = ''
        if target:
            target_str += '{}'.format(ReadDataStatement.get_target_expr(target))
        if target and column:
            connect_str += '='
        if column:
            if sasoptpy.util.has_expr(column):
                column_str += 'col(' + column._expr() + ')'
            else:
                column_str += '{}'.format(column)

        # If both equal, no need for second part
        if target_str == column_str:
            connect_str = ''
            column_str = ''

        s = target_str + connect_str + column_str

        if index and sasoptpy.abstract.util.is_key_abstract(index):
            s = '{{{}}} < {} >'.format(sasoptpy.to_definition(index), s)

        return s

    @classmethod
    def get_target_expr(cls, target):
        return sasoptpy.to_expression(target)

    def _defn(self):
        s = 'read data '
        table_str = self.get_table_expr()
        index_str = self.get_index_expr()
        col_str = self.get_columns_expr()

        s += table_str + ' into'
        if index_str != '':
            s += ' ' + index_str
        if self._columns is not None:
            s += ' ' + col_str
        s += ';'
        return s

    @classmethod
    def read_data(cls, *args, **kwargs):
        r = ReadDataStatement(*args, **kwargs)
        return r