import gdata
from gdata.data import BatchFeed
from gdata.spreadsheets.client import SpreadsheetsClient
from gdata.spreadsheets.data import ListEntry, CellsFeed, ListsFeed

from spreadsheetdb.exception import SpreadSheetDBError, SpreadSheetNotExists
from spreadsheetdb.field import Field
from spreadsheetdb.settings import username, password, source, spreadsheet_key


class SpreadSheetDBConnection(object):

    def __init__(self, username, password, spreadsheet_key=None, source="SpreadSheetDBConnection"):
        self._username = username
        self._password = password
        self._spreadsheet_key = spreadsheet_key
        self._source = source
        self._is_connected = False
        self._worksheets = []
        self._client = SpreadsheetsClient()
        #self._tables = []

    def connect(self, spreadsheet_key=None):
        if self._is_connected:
            raise SpreadSheetDBError()
        if spreadsheet_key:
            self._spreadsheet_key = spreadsheet_key

        if not self._spreadsheet_key:
            raise SpreadSheetDBError()
        self._client.client_login(self._username, self._password, source=self._source)
        self._is_connected = True
        self.select_spreadsheet(self._spreadsheet_key)

    def select_spreadsheet(self, spreadsheet_key):
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

            #list_feed = self._client.get_list_feed(self._spreadsheet_key, worksheet.get_worksheet_id())
            #for row in list_feed.entry:
            #    print row.title.text, row.content
        #
        #tables = self._client.get_tables(self._spreadsheet_key)
        #for table in tables.entry:
        #    self._tables[table.title.text] = table.get_table_id()
        #print self._worksheets

    def create_list(self, model):
        if not self._is_connected:
            raise SpreadSheetDBError()

        list_name = getattr(model, "table_name")()
        if not list_name:
            raise SpreadSheetDBError()
        fieils = []
        for index, value in model.__dict__.iteritems():
            if isinstance(value, Field):
                fieils.append(index)
        #if not table_name in self._tables.iteritems():
        #self._refresh_worksheets_info()
        #self._client.get_cell(self._spreadsheet_key, self._worksheets[])
        #
        #self._client.add_table(self._spreadsheet_key, table_name, description, table_name, 1, len(list(fields_dict.keys())), 0,
        #                   "insert", fields_dict)

        if not list_name in self._worksheets.iterkeys():
            worksheet = self._client.add_worksheet(self._spreadsheet_key, list_name, 1, len(fieils))
            self._worksheets[worksheet.title.text] = {'key': worksheet.get_worksheet_id(), 'row_count': worksheet.row_count.text,
                                                              'col_count': worksheet.col_count.text}
        cell_feed = gdata.spreadsheets.data.build_batch_cells_update(
        self._spreadsheet_key, self._worksheets[list_name]['key'])
        col = 1
        for index in fieils:
            cell_feed.add_set_cell(1, col, index)
            col += 1
        self._client.batch(cell_feed, force=True)
        #return self._worksheets[list_name]

    def add_entry(self, list_name, fields):
        """Adds a new row to the worksheet's list feed.

        Args:
          list_entry: gdata.spreadsheets.data.ListsEntry An entry which contains
                      the values which should be set for the columns in this
                      record.
          spreadsheet_key: str, The unique ID of this containing spreadsheet. This
                           can be the ID from the URL or as provided in a
                           Spreadsheet entry.
          worksheet_id: str, The unique ID of the worksheet in this spreadsheet
                        whose cells we want. This can be obtained using
                        WorksheetEntry's get_worksheet_id method.
          auth_token: An object which sets the Authorization HTTP header in its
                      modify_request method. Recommended classes include
                      gdata.gauth.ClientLoginToken and gdata.gauth.AuthSubToken
                      among others. Represents the current user. Defaults to None
                      and if None, this method will look for a value in the
                      auth_token member of SpreadsheetsClient.
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

    def delete_entry(self, entry):
        self._client.delete(entry)

    def all_entries(self, list_name):
        list_feed = self._client.get_list_feed(self._spreadsheet_key, self._worksheets[list_name]['key'])
        return list_feed.entry


connection = SpreadSheetDBConnection(username, password, source=source, spreadsheet_key=spreadsheet_key)