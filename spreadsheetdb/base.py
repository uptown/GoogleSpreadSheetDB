from spreadsheetdb.backend import connection as default_connection
from spreadsheetdb.field import Field
from spreadsheetdb.exception import SpreadSheetNotExists, EntryAlreadyExists
from gdata.spreadsheets.data import ListEntry


class ModelManager(object):

    def set_cls(self, cls):
        self._model_cls = cls



class ModelBase(type):

    def __new__(cls, name, bases, dct):
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super(ModelBase, cls).__new__(cls, name, bases, dct)
        if not '_fields' in dct:
            _fields = []
            for index, value in dct.iteritems():
                if isinstance(value, Field):
                    _fields.append(index)
            cls._fields = _fields

        return super(ModelBase, cls).__new__(cls, name, bases, dct)


class Model(object):

    objects = ModelManager()
    __metaclass__ = ModelBase

    def __init__(self, **kwargs):
        self._entry = None
        self._data = {}
        self._all_fields = getattr(self.__class__, '_fields')
        for index, value in kwargs.iteritems():
            if index in self._all_fields:
                self._data[index] = value
            elif isinstance(value, ListEntry):
                for field in self._all_fields:
                    self._data[field] = value.get_value(field)
                self._entry = value

        for field in self._all_fields:
            setattr(self, field, self._data.get(field))

    def save(self, connection=None):
        if not connection:
            connection = default_connection
        if self._entry:
            raise EntryAlreadyExists()
        for field in self._all_fields:
            if not field in self._data:
                self._data[field] = str(getattr(getattr(self.__class__, field), 'default'))
            else:
                self._data[field] = str(self._data[field])
        try:
            self._entry = connection.add_entry(self.__class__.table_name(), self._data)
        except SpreadSheetNotExists:
            connection.create_list(self.__class__)
            self._entry = connection.add_entry(self.__class__.table_name(), self._data)

    def delete(self, connection=None):
        if not connection:
            connection = default_connection
        connection.delete_entry(self._entry)
        self._entry = None

    @classmethod
    def all(cls, connection=None):
        if not connection:
            connection = default_connection
        feed = connection.all_entries(cls.table_name())
        return [cls(entry=entry) for entry in feed]

    @classmethod
    def table_name(cls):
        return cls.__name__

    def __getattr__(self, item):
        print item, 'asd'
        return super(Model, self).__getattr__(self, item)