from app import app

import unittest
import os


# you can search through the file for TEST-###
class BasicTestCase(unittest.TestCase):
    # TEST-001
    # def test_index(self):
        # tester = app.test_client(self)
        # response = tester.get('/', content_type='html/text')
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data, b'Hello, World!')
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_database(self):
        tester = os.path.exists("flaskr.db")
        self.assertTrue(tester)


if __name__ == '__main__':
    unittest.main()
