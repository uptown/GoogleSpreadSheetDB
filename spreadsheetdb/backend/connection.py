import gdata
from gdata.spreadsheets.client import SpreadsheetsClient, ListQuery
from gdata.spreadsheets.data import ListEntry, ListsFeed

from spreadsheetdb.exception import SpreadSheetDBError, SpreadSheetNotExists
from spreadsheetdb.field import Field


class SpreadSheetDBConnection(object):
    """
    Spreadsheet wrapper class
    """
    default_connection = None

    def __init__(self, username=None, password=None, spreadsheet_key=None, source="SpreadSheetDBConnection"):
        self._username = username
        self._password = password
        self._spreadsheet_key = spreadsheet_key
        self._source = source
        self._is_connected = False
        self._worksheets = []
        self._client = SpreadsheetsClient()
        #self._tables = []

    def connect(self, username=None, password=None, spreadsheet_key=None, source="SpreadSheetDBConnection"):
        """
        make a connection with google api, and load spreadsheet information.
        """
        if self._is_connected:
            raise SpreadSheetDBError()
        if spreadsheet_key:
            self._spreadsheet_key = spreadsheet_key
        if username:
            self._username = username
        if password:
            self._password = password
        if source:
            self._source = source
        if not self._spreadsheet_key or not self._username or not self._password or not  self._source:
            raise SpreadSheetDBError()
        self._client.client_login(self._username, self._password, source=self._source)
        self._is_connected = True
        self.select_spreadsheet(self._spreadsheet_key)

    def select_spreadsheet(self, spreadsheet_key):
        """
        select spreadsheet
        """
        if not self._is_connected:
            raise SpreadSheetDBError()
        self._worksheets = {}
        if spreadsheet_key:
            self._spreadsheet_key = spreadsheet_key
        self._refresh_worksheets_info()

    def _refresh_worksheets_info(self):
        if not self._is_connected:
            raise SpreadSheetDBError()

        if not self._spreadsheet_key:
            raise SpreadSheetDBError()

        worksheets = self._client.get_worksheets(self._spreadsheet_key)
        for worksheet in worksheets.entry:
            self._worksheets[worksheet.title.text] = {'key': worksheet.get_worksheet_id(), 'row_count': worksheet.row_count.text,
                                                      'col_count': worksheet.col_count.text}

    def create_list(self, model):
        """
        make a new worksheet for model
        """
        if not self._is_connected:
            raise SpreadSheetDBError()

        list_name = getattr(model, "worksheet_name")()
        if not list_name:
            raise SpreadSheetDBError()
        fields = []
        for index, value in model.__dict__.iteritems():
            if isinstance(value, Field):
                fields.append(index)

        if not list_name in self._worksheets.iterkeys():
            worksheet = self._client.add_worksheet(self._spreadsheet_key, list_name, 1, len(fields))
            self._worksheets[worksheet.title.text] = {'key': worksheet.get_worksheet_id(), 'row_count': worksheet.row_count.text,
                                                      'col_count': worksheet.col_count.text}
        cell_feed = gdata.spreadsheets.data.build_batch_cells_update(
        self._spreadsheet_key, self._worksheets[list_name]['key'])
        col = 1
        for index in fields:
            cell_feed.add_set_cell(1, col, index)
            col += 1
        self._client.batch(cell_feed, force=True)

    def add_entry(self, list_name, fields):
        """
        add new entry to worksheet
        """
        if not self._is_connected:
            raise SpreadSheetDBError()
        try:
            current_worksheet = self._worksheets[list_name]
        except KeyError:
            raise SpreadSheetNotExists()
        inserting_row = ListEntry()
        for key, val in fields.iteritems():
            inserting_row.set_value(key, val)
        ret = self._client.add_list_entry(inserting_row, self._spreadsheet_key, current_worksheet['key'])
        #self._client.delete(ret)
        #list_feed = self._client.get_list_feed(self._spreadsheet_key, self._worksheets[list_name]['key'])
        #for entry in list_feed.entry:
            #self._client.delete(entry)
        #print list_feed
        return ret

    def update_entry(self, entry, data):
        """
        update entry
        """
        for key, val in data.iteritems():
            entry.set_value(key, val)
        self._client.update(entry)

    def delete_entry(self, entry):
        """
        delete entry
        """
        self._client.delete(entry)

    def all_entries(self, list_name):
        """
        load all entries from worksheet.
        """
        list_feed = self._client.get_list_feed(self._spreadsheet_key, self._worksheets[list_name]['key'])
        return list_feed.entry

    def filtered_entries(self, list_name, sq=None, order_by=None, reverse=None):
        """
        load filtered entries
        https://developers.google.com/google-apps/spreadsheets/?hl=uk-UA&csw=1#sending_a_structured_query_for_rows
        """
        query = ListQuery(order_by=order_by, reverse=reverse, sq=sq)
        list_feed = self._client.get_list_feed(self._spreadsheet_key, self._worksheets[list_name]['key'], query=query)
        return list_feed.entry

SpreadSheetDBConnection.default_connection = SpreadSheetDBConnection()
connection = SpreadSheetDBConnection.default_connection