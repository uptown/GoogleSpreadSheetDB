from spreadsheetdb.backend import connection as default_connection
from spreadsheetdb.field import Field
from spreadsheetdb.exception import SpreadSheetNotExists, EntryAlreadyExists, EntryNotExists
from gdata.spreadsheets.data import ListEntry


_all_fields_for_model = {}

def all_fields_for_model(cls):
    ret = _all_fields_for_model.get(cls.__name__)
    if ret:
        return _all_fields_for_model.get(cls.__name__)
    ret = []
    for index, value in cls.__dict__.iteritems():
        if isinstance(value, Field):
            ret.append(index)
    _all_fields_for_model[cls.__name__] = ret
    return ret


class Model(object):

    def __init__(self, **kwargs):
        self._entry = None
        self._all_fields = all_fields_for_model(self.__class__)
        for index, value in kwargs.iteritems():
            if index in self._all_fields:
                setattr(self, index, value)
            elif isinstance(value, ListEntry):
                for field in self._all_fields:
                    setattr(self, field, value.get_value(field))
                self._entry = value
                break

    def save(self, connection=None):
        """
        save object to google spreadsheet,
        after save, self._entry store ListEntry Object.
        @param connection: spreadsheet connection if need
        @raise EntryAlreadyExists: the object is already saved
        """
        if not connection:
            connection = default_connection
        _data = {}
        if self._entry:
            raise EntryAlreadyExists()
        for field in self._all_fields:
            val = getattr(self, field)
            if not isinstance(val, Field):
                _data[field] = val
            else:
                _data[field] = str(getattr(getattr(self.__class__, field), 'default'))
        try:
            self._entry = connection.add_entry(self.__class__.table_name(), _data)
        except SpreadSheetNotExists:
            connection.create_list(self.__class__)
            self._entry = connection.add_entry(self.__class__.table_name(), _data)

    def delete(self, connection=None):
        """
        delete object form google spreadsheet.
        if self._entry is None, raise EntryNotExists
        @param connection: spreadsheet connection if need
        @raise EntryNotExists: the object entry does not exist
        """
        if not connection:
            connection = default_connection
        if self._entry:
            raise EntryNotExists()
        connection.delete_entry(self._entry)
        self._entry = None

    @classmethod
    def all(cls, connection=None):
        """
        fetch all entries
        @param connection: spreadsheet connection if need
        @return: model list
        """
        if not connection:
            connection = default_connection
        feed = connection.all_entries(cls.table_name())
        return [cls(entry=entry) for entry in feed]

    @classmethod
    def table_name(cls):
        """
        if you want specific worksheet name, override this method
        @return: table_name
        """
        return cls.__name__
