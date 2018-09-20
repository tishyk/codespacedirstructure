# help is here https://docs.pytest.org/en/latest/builtin.html
# Lets verify:
#    db.get_entry(10,2017) == (2017, 10, 102.5)
#    db.current_month_entry == (2017, 12, 100.5)
#    db.last_entry == (2017, 12, 100.5)

from .database import Database
from pytest import fixture


# class TestDatabase():
# # py.test -v -rxs -k entry
#     @fixture
#     def my_setup(self):
#         db = Database()
#         return db
#
#     def test_get_entry(self,my_setup):
#         assert db.get_entry(10, 2017) == (2017, 10, 102.5)
#
#     def test_current_month_entry(self,my_setup):
#         assert db.current_month_entry == (2017, 12, 100.5)
#
#     def test_last_entry(self,my_setup):
#         assert db.last_entry == (2017, 12, 100.5)

class TestDatabaseSetup():
    # cmd - py.test -v -rxs -k entry --capture=no
    @fixture    # fixture(scope="module")
    def db_object(self):
        print('Connect to DB\n')
        db = Database()
        #return db
        yield db
        print("Close connection")
        db.close()

    def test_get_entry(self, db_object):
        assert db_object.get_entry(10, 2017) == (2017, 10, 102.5)

    def test_current_month_entry(self, db_object):
        assert db_object.current_month_entry == (2017, 12, 100.5)

    def test_last_entry(self, db_object):
        assert db_object.last_entry == (2017, 12, 100.5)
