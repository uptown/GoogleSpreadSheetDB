from spreadsheetdb.backend.connection import connection
from spreadsheetdb.base import Model
from spreadsheetdb.field import DynamicField


class TestModel4(Model):
    test1 = DynamicField(default="")
    test5 = DynamicField(default="default")
    test3 = DynamicField(default=1)
    test2 = DynamicField(default="default3")
    test4 = DynamicField(default=True)
    test55 = DynamicField(default="??")


class TestModel1(Model):
    asdasdasd = DynamicField(default="")
    asdasdasad = DynamicField(default="asd")



connection.connect(username=username, password=password, source=source, spreadsheet_key=spreadsheet_key)
for each in TestModel4.filter(sq="test1!=asd"):
    print each.test1

for each in TestModel4.filter(sq="test1=asd"):
    print each.test1
#test = TestModel4(test1="asd")
#test.save()
#test = TestModel4(test1="22")
#test.save()
#test = TestModel4(test1="33")
#test.save()
#i = 1
#for val in TestModel4.all():
#    val.test55 = i
#    i += 1
#    val.save()
#
#test2 = TestModel1(asdasdasd="aaaaa")
#test2.save()
#test.delete()