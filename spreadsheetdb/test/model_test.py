from spreadsheetdb.backend import connection
from spreadsheetdb.base import Model
from spreadsheetdb.field import DynamicField


class TestModel4(Model):
    test1 = DynamicField(default="")
    test5 = DynamicField(default="default")
    test3 = DynamicField(default=1)
    test2 = DynamicField(default="default3")
    test4 = DynamicField(default=True)


connection.connect()
test = TestModel4(test1="asd")
test.save()
test = TestModel4(test1="22")
test.save()
test = TestModel4(test1="33")
test.save()
for val in TestModel4.all():
    print val.test1
#test.delete()