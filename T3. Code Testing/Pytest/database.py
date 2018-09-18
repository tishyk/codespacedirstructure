import sqlite3
from datetime import datetime
from distutils.version import LooseVersion


class Database():
    def __init__(self, dbname='ukrstatdb', table_name='Inflation'):
        self.conn = None
        self.cursor = None
        self.dbname = dbname
        self.table_name = table_name
        self.__open(dbname)
        self.__create_new()
        self.current_date = datetime.now()

    def __open(self, dbname):
        try:
            self.conn = sqlite3.connect(dbname)
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            print("Local Database connection Error!")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __create_new(self):
        """Create new table if it's not exists"""
        query = 'CREATE TABLE IF NOT EXISTS {0} \
        (year INTEGER PRIMARY KEY, month INTEGER,  inflation REAL);'.format(self.table_name)
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_entries(self, columns='*'):
        """Extract all data columns from  Database Table"""
        query = 'SELECT {1} FROM {0};'.format(self.table_name, columns)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    @property
    def last_entry(self):
        """Get last data entry from Database Table"""
        return self.get_all_entries()[-1]

    @property
    def current_month_entry(self):
        """Get current month data entry from Database Table. None if not exists"""
        return self.get_entry(self.current_date.month, self.current_date.year)

    def get_entry(self, month, year):
        """Get data entry from Database Table"""
        query = 'SELECT * FROM {0} where year={1} and month={2};'.format(self.table_name, year, month)
        self.cursor.execute(query)
        rows = self.cursor.fetchone()
        return rows

    def period_entries(self, start=(2007, 1), end=None):
        if not end: end = (self.current_date.year, self.current_date.month)
        lv_str = lambda t: '.'.join((str(s) for s in t))
        entries = []
        for entry in self.get_all_entries():
            if (LooseVersion(lv_str(start)) <= LooseVersion(lv_str(entry[:2])) and
                        LooseVersion(lv_str(end)) >= LooseVersion(lv_str(entry[:2]))):
                entries.append(entry)
        return entries

    def write_entry(self, year, month, data):
        """Insert data into Table"""
        query = 'INSERT INTO {0} VALUES ( {1}, {2}, {3});'.format(self.table_name, year, month, data)
        self.cursor.execute(query)
        self.conn.commit()

    def __query(self, sql):
        """Execution method for random query"""
        self.cursor.execute(sql)
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection to DataBase"""
        self.close()


if __name__ == "__main__":
    db = Database()
    print(db.get_entry(10, 2017))
    print(db.current_month_entry)
    print(db.last_entry)
