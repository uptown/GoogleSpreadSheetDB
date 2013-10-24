
class SpreadSheetDBError(Exception):
    """
    Global Error
    """
    pass


class FieldError(SpreadSheetDBError):
    """
    Error From Field
    """
    pass


class SpreadSheetNotExists(SpreadSheetDBError):
    """
    Spreadsheet key is not valid.
    """
    pass


class EntryAlreadyExists(SpreadSheetDBError):
    """
    Entry is already saved
    """
    pass


class EntryNotExists(SpreadSheetDBError):
    """
    Entry is not specified.
    """
    pass