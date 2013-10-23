
class SpreadSheetDBError(Exception):
    pass


class FieldError(Exception):
    pass


class SpreadSheetNotExists(SpreadSheetDBError):
    pass


class EntryAlreadyExists(SpreadSheetDBError):
    pass


class EntryNotExists(SpreadSheetDBError):
    pass