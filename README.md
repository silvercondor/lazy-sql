# LazySql: Sql connector for lazy people

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
query2 = f"INSERT * INTO write_table(value1, value2, value3) VALUES(%s, %s, %s)"
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
