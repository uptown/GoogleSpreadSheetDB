#!/usr/bin/env python
# coding: utf-8
"""
    spreadsheetdb
    ~~~~~~~~~~~~~
    This module is for using google spreadsheet as a data-source.
    To use, you must install gdata-python-client (https://code.google.com/p/gdata-python-client/)
    (This code was developed with gdata-python-client 2.0.18)

    example)

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
    TestModel1(test_field0="test").save()

    You can check more samples in spreadsheetdb.test.


    :license: MIT License, see LICENSE for more details
"""

__author__ = 'uptown(uptownlee89@gmail.com'
__copyright__ = 'Copyright (c) 2013 Juyoung Lee'
__version__ = '0.1.0'
