# -*- coding: utf-8 -*-
from spreadsheetdb.exception import FieldError


class Field(object):
    """
    Base Field Class
    """
    def __init__(self, **kwargs):
        all_keys = kwargs.iterkeys()
        if "default" in all_keys:
            if kwargs['default'] is None:
                raise FieldError()
            self._default=kwargs['default']
            self._has_default = True
        else:
            self._has_default = False

        self._field_name = kwargs.get('field_name', None)

    @property
    def field_name(self):
        """
        if field_name is not null, the field will represent field_name in the worksheet.
        @return:
        """
        return self._field_name

    @property
    def default(self):
        """
        return default value if exists or raise FieldError
        """
        if not self.has_default:
            raise FieldError()
        return self._default

    @property
    def has_default(self):
        return self._has_default


class DynamicField(Field):
    """
    dynamicField
    """
    pass