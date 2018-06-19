# general imports
import unittest
import os
import tempfile

# project (local) imports
import app


# you can search through the file for TEST-###
class BasicTestCase(unittest.TestCase):
    # TEST-001
    def test_index(self):
        """ Initial test: Ensure Flask is set up correctly and running properly. """
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

    # TEST-002
    # def test_index(self):
        # tester = app.test_client(self)
        # response = tester.get('/', content_type='html/text')
        # self.assertEqual(response.status_code, 404)

    # TEST-003
    def test_database(self):
        """ Initial test: Ensure that the database exists. """
        tester = os.path.exists("flaskr.db")
        self.assertTrue(tester, True)


class FlaskrTestCase(unittest.TestCase):
    # TEST-004
    def setUp(self):
        """ Set up a blank tmp database before each test. """
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    # TEST-004
    def tearDown(self):
        """ Destroy the blank tmp database after each test. """
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    # TEST-004
    def login(self, username, password):
        """ Login helper function """
        return self.app.post('/login', data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)

    # TEST-004
    def logout(self):
        """ Logout helper funtion """
        return self.app.get('/logout', follow_redirects=True)

    # TEST-004
    # assert functions
    def test_empty_db(self):
        """ Ensure database is blank """
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    # TEST-004
    def test_login_logout(self):
        """ Test login and logout using the helper functions """
        # testing successful login
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        assert b'You were logged in' in rv.data
        # testing successful logout
        rv = self.logout()
        assert b'You were logged out' in rv.data
        # testing invalid username with correct password
        rv = self.login(
            app.app.config['USERNAME'] + 'x',
            app.app.config['PASSWORD']
        )
        assert b'Invalid username' in rv.data
        # testing invalid password with correct username
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD'] + 'x'
        )
        assert b'Invalid password' in rv.data

    # TEST-004
    def test_messages(self):
        """ Ensure that a user can post messages. """
        self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()
