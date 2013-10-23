from spreadsheetdb.exception import FieldError


class Field(object):

    def __init__(self, **kwargs):
        allkeys = kwargs.iterkeys()
        if "default" in allkeys:
            if kwargs['default'] is None:
                raise FieldError()
            self._default=kwargs['default']
            self._has_default = True
        else:
            self._has_default = False

    @property
    def default(self):
        if not self.has_default:
            raise FieldError()
        return self._default

    @property
    def has_default(self):
        return self._has_default


class DynamicField(Field):
    pass