Google Spreadsheet wrapper 0.1
=====================================
This module is for using google spreadsheet as a data-source.

Pre-required
====================================
gdata-python-client 2.0.18(https://code.google.com/p/gdata-python-client/)

Example
====================================
    from spreadsheetdb.backend import connection
    from spreadsheetdb.base import Model
    from spreadsheetdb.field import DynamicField

    class TestModel1(Model):
        test_field0 = DynamicField(default="")
        test_field1 = DynamicField(default="asd")

    #google username, google password
    #source is a string for tracking. You can use any string
    #spreadsheet_key is pk for targeted spreadsheet

    connection.connect(username=username, password=password, source=source, spreadsheet_key=spreadsheet_key)
    test = TestModel1(test_field0="test").save()
    test = TestModel1(test_field0="test1").save()
    test = TestModel1(test_field0="test2").save()
    test = TestModel1(test_field0="test3").save()
    test = TestModel1(test_field0="test4").save()
    print TestModel1.filter(test_field0="test")[0].test_field0
    test.delete()

TO DO
=====================================
Lazy entry feed.
Aggregate request.
...
