import unittest
import test_sql


class TestTestaton(unittest.TestCase):
    def setUp(self):
        pass

    def test_script1(self):
        script = test_sql.TestScript('testSql.sql')

        print(script.all_tests_sql)

        sql1 = script.all_tests_sql[0]

        self.assertEqual(sql1.index, ['market_id']) 
        self.assertEqual(sql1.measurements, ['percentage'])
        self.assertIsNone(sql1.airline)


        sql2 = script.all_tests_sql[1]
        self.assertEqual(sql2.sql_text.strip(),
            "select sysdate from dual")


if __name__ == '__main__':
    unittest.main()
