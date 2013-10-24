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