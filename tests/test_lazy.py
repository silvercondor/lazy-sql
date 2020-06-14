import os
import sys
import sqlite3
import unittest
import lazysql
from lazysql import LazySql


class TestLazySql(unittest.TestCase):

    def setUp(self):
        if 'lazysql_test.db' in os.listdir():
            exit('lazysql_test.db already exists in current working directory.\nDelete the current instance or pick another directory to run test.')
        os.system('touch lazysql_test.db')

        with sqlite3.connect('lazysql_test.db') as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE test(
                        id INTEGER PRIMARY KEY,
                        _str STRING NOT NULL,
                        _int INTEGER NOT NULL,
                        _float FLOAT NOT NULL);""")
            conn.commit()
            for i in range(0, 10):
                cur.execute(
                    f"INSERT INTO test(_str, _int, _float) VALUES('test{i}', {i}, {i+0.5});")
            conn.commit()
        self.db = LazySql(sqlite3, 'lazysql_test.db')
        print('Setup complete, starting tests...')

    def tearDown(self):
        try:
            os.system('rm -rf lazysql_test.db')
            return True
        except Exception as e:
            print(e)
            return False

    def test_read(self):
        res = self.db.query("SELECT * FROM test WHERE _str='test1';")
        data = res[0]
        self.assertEqual(data['_str'], 'test1')
        self.assertEqual(data['_int'], 1)
        self.assertEqual(data['_float'], 1.5)

    def test_read_non_existant_data(self):
        res = self.db.query("SELECT * FROM test WHERE _str='invalidString';")
        self.assertEqual(res, [])

    def test_read_invalid_query(self):
        res = self.db.query(
            "SELECT invalid_table FROM test WHERE _str='test1';")
        self.assertEqual(res, False)

    def test_write(self):
        write_res = self.db.query(
            "INSERT INTO test(_str, _int, _float) VALUES('test11', 11, 11.5);", commit=True)
        read_res = self.db.query("SELECT * FROM test WHERE _str='test11';")
        data = read_res[0]
        self.assertEqual(write_res, True)
        self.assertEqual(data['_str'], 'test11')
        self.assertEqual(data['_int'], 11)
        self.assertEqual(data['_float'], 11.5)

    def test_async_read(self):
        queries = [{"query": f"SELECT * FROM test WHERE _str=?;", "data": [f"test{n}"]}
                   for n in range(1, 4)]
        res = self.db.async_query(queries)
        for i, q in enumerate(res):
            i += 1
            self.assertEqual(q[0]['_str'], f"test{i}")
            self.assertEqual(q[0]['_int'], i)
            self.assertEqual(q[0]['_float'], i+0.5)

    def test_async_read_with_non_existant_data(self):
        queries = [{"query": f"SELECT * FROM test WHERE _str=?;", "data": [f"test{n}"]}
                   for n in range(1, 4)]
        # Overwrite to make query2 error
        queries[1]['query'] = "SELECT * FROM test WHERE _str=?;"
        queries[1]['data'] = ['test11']
        query1, query2, query3 = self.db.async_query(queries)
        self.assertEqual(query1[0]['_str'], f"test1")
        self.assertEqual(query1[0]['_int'], 1)
        self.assertEqual(query1[0]['_float'], 1.5)
        self.assertEqual(query2, [])
        self.assertEqual(query3[0]['_str'], f"test3")
        self.assertEqual(query3[0]['_int'], 3)
        self.assertEqual(query3[0]['_float'], 3.5)

    def test_async_read_with_invalid_query(self):
        queries = [{"query": f"SELECT * FROM test WHERE _str=?;", "data": [f"test{n}"]}
                   for n in range(1, 4)]
        # Overwrite to make query2 error
        queries[1]['query'] = "SELECT * FROM invalid_table WHERE _str=?;"
        query1, query2, query3 = self.db.async_query(queries)
        self.assertEqual(query1[0]['_str'], f"test1")
        self.assertEqual(query1[0]['_int'], 1)
        self.assertEqual(query1[0]['_float'], 1.5)
        self.assertEqual(query2, False)
        self.assertEqual(query3[0]['_str'], f"test3")
        self.assertEqual(query3[0]['_int'], 3)
        self.assertEqual(query3[0]['_float'], 3.5)


if __name__ == '__main__':
    unittest.main()
