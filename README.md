# LazySql: SQL connector for lazy people

## Installation

```
pip3 install lazysql
```

---

## Usage

### Connecting

```
#Import your db connector
import sqlite3
import psycopg2
from lazysql import LazySql

read_db = LazySql(sqlite3, 'read.db',)

write_db = LazySql(psycopg2, "dbname='write_db' user='postgres' host='localhost' password='UnsafePassword' port=5432")
```

---

### Reading

```
query1 = f"SELECT * FROM read_table LIMIT 5;"
#Returns selection from DB
res = read_db.query(query1)
```

---

### Writing

```
query2 = f"INSERT INTO write_table(value1, value2, value3) VALUES(%s, %s, %s)"
write_db.query(query2, , data=(test, 1, 2.3), commit=True)
```

---

### Batch Writing

```
query3 = f"INSERT INTO write_table(value1, value2, value3) VALUES(%s, %s, %s)"
for i in range(0,100):
    write_db.batch(query3, data=(f"test{i}", i, i+1.5))
write_db.commit()


#Alternatives
write_db.batch(None, commit=True) #Commits directly
write_db.close() #Close without committing
write_db.batch(None, close=True) #Close without committing
```

---

### Async

```
read_db.async_query([
    {"query":"SELECT * FROM test WHERE _str='test1},
    {"query":"SELECT * FROM test WHERE _str='test2},
    {"query":"SELECT * FROM test WHERE _str='test3}
])

#Result will be in list of order of query sent
#i.e
[
    [
        {'id': 5, '_str': 'test1', '_int': 1, '_flt': 2.5},
        {'id': 15, '_str': 'test1', '_int': 1, '_flt': 2.5},
        {'id': 25, '_str': 'test1', '_int': 1, '_flt': 2.5}],
    [
        {'id': 6, '_str': 'test2', '_int': 2, '_flt': 3.5},
        {'id': 16, '_str': 'test2', '_int': 2, '_flt': 3.5},
        {'id': 26, '_str': 'test2', '_int': 2, '_flt': 3.5}
    ],
    [
        {'id': 7, '_str': 'test3', '_int': 3, '_flt': 4.5},
        {'id': 17, '_str': 'test3', '_int': 3, '_flt': 4.5},
        {'id': 27, '_str': 'test3', '_int': 3, '_flt': 4.5}]
]
```
