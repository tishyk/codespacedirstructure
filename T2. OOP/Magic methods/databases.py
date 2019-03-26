

class Connection:
    def __new__(cls, *args, **kwargs):
        print("New connection object creation")
        return super().__new__(cls)

    def __init__(self, db_type, path):
        self.db_type = db_type
        self.db_path = path
        self.records = range(100000)

    def __format__(self, format_spec):
        return "incoming format string {} for current connection".format(format_spec)  #recursion --> self

    def __dir__(self):
        return [self.db_type]

    def __round__(self, n=None):
        if n:
            records = self.records[:n]
        return records

    def __iter__(self):
        print("Get all records range")
        return self.records
        #yield from self.records

    def __getitem__(self, item):
        return self.records[item]

    def __irecords(self):
        for record in self.records:
            yield record

    def get_record(self, n):
        return range(n)

postgre_sql = Connection('postgresql','./postgresql/connection.db')
my_sql = Connection('postgresql','./postgresql/connection.db')
# Representation
print(postgre_sql)
print("This is a {}".format(postgre_sql))
print(dir(my_sql))
# Compare db connections
# Unary operators: -my_sql --> get all db records --> +my_sql
print(round(postgre_sql, 20))
# Math operators: postgre_sql + my_sql
# Recursive math operations: postgre_sql + my_sql
# Augmented assignment operations: postgre_sql += alternative_db_path
# Type conversation: int(my_sql) --> len(my_sql.records)
# Context manager:
# with Connection('sqlite','./sqlite/connection.db') as sqlite:
#     sqlite.get_record(10)
# Iterable object:
#print(iter(my_sql))

for ms in my_sql:        #[:8]:
     print(ms)





