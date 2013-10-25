# -*- coding: utf-8 -*-
from spreadsheetdb.backend.connection import SpreadSheetDBConnection, ListEntry
from spreadsheetdb.field import Field
from spreadsheetdb.exception import SpreadSheetNotExists, EntryNotExists


_all_fields_for_model = {}
default_connection = SpreadSheetDBConnection.default_connection


def all_fields_for_model(cls):
    """
    @todo: check
    """
    if _all_fields_for_model.get(cls.__name__):
        return _all_fields_for_model.get(cls.__name__)
    ret = []
    names_dict = {}
    for index, value in cls.__dict__.iteritems():
        if isinstance(value, Field):
            ret.append(index)
            names_dict[index] = value.field_name if value.field_name else index
    _all_fields_for_model[cls.__name__] = ret, names_dict
    return ret, names_dict


class Model(object):

    def __init__(self, **kwargs):
        self._entry = None
        self._all_fields, self._names_dict = all_fields_for_model(self.__class__)
        for index, value in kwargs.iteritems():
            if index in self._all_fields:
                setattr(self, index, value)
            elif isinstance(value, ListEntry):
                for field in self._names_dict.iterkeys():
                    setattr(self, self._names_dict[field], value.get_value(field))
                self._entry = value
                break

    def save(self, connection=None):
        """
        save object to google spreadsheet,
        after save, self._entry store ListEntry Object.
        @param connection: spreadsheet connection if need
        """
        if not connection:
            connection = default_connection
        if self._entry:
            self.update(connection=connection)
        else:
            _data = self._construct_data()
            try:
                self._entry = connection.add_entry(self.__class__.worksheet_name(), _data)
            except SpreadSheetNotExists:
                connection.create_list(self.__class__)
                self._entry = connection.add_entry(self.__class__.worksheet_name(), _data)

    def update(self, connection=None):
        """
        update entry
        @param connection: spreadsheet connection if need
        @raise EntryNotExists: entry is not set
        """
        if not connection:
            connection = default_connection
        if not self._entry:
            raise EntryNotExists()
        _data = self._construct_data()
        connection.update_entry(self._entry, _data)

    def _construct_data(self):
        _data = {}
        for field in self._all_fields:
            val = getattr(self, field)
            if not isinstance(val, Field):
                _data[self._names_dict[field].decode("utf8")] = str(val).decode("utf8")
            else:
                _data[self._names_dict[field].decode("utf8")] = str(getattr(getattr(self.__class__, field), 'default')).decode("utf8")
        return _data

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
    def filter(cls, sq=None, order_by=None, reverse=None, connection=None):
        if not connection:
            connection = default_connection
        feed = connection.filtered_entries(cls.worksheet_name(), sq=sq, order_by=order_by, reverse=reverse)
        return [cls(entry=entry) for entry in feed]

    @classmethod
    def all(cls, connection=None):
        """
        fetch all entries
        @param connection: spreadsheet connection if need
        @return: model list
        """
        if not connection:
            connection = default_connection
        feed = connection.all_entries(cls.worksheet_name())
        return [cls(entry=entry) for entry in feed]

    @classmethod
    def worksheet_name(cls):
        """
        if you want specific worksheet name, override this method
        @return: worksheet_name
        """
        return cls.__name__
