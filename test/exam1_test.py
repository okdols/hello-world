# exam1_test.py
import os
import unittest
import tempfile
from sys import path

from flask import Flask, request, app, json

import exam1

app = Flask(__name__)
app.config.from_object(__name__)


# Reference: https://damyanon.net/flask-series-testing/
# Flask app unittest
class TestsCase(unittest.TestCase):
    test_id = ""

    # Initialization logic for the test suite declared in the test module.
    # Code that is executed before all tests in one test run.
    @classmethod
    def setUpClass(self):
        # Create test DB temporary
        self.db_fd, exam1.app.config['DATABASE'] = tempfile.mkstemp()
        exam1.app.config['TESTING'] = True
        self.app = exam1.app.test_client()

    # Clean up logic for the test suite declared in the test module.
    # Code that is executed after all tests in one test run.
    @classmethod
    def tearDownClass(self):
        # Delete test DB
        os.close(self.db_fd)
        os.unlink(exam1.app.config['DATABASE'])

    # Initialization logic
    # Code that is executed before each test.
    def setUp(self):
        # Create test client
        self.app = exam1.app.test_client()
        # Propagate the exceptions to the test client.
        self.app.testing = True

    # Code that is executed after each test.
    def tearDown(self):
        pass

    # Sends HTTP request to the application on the specified path.
    # Check HTTP success status code(200) and response using 'assert' method.

    # HTTP POST case: new user
    def test_01_post(self):
        # Using test package.
        result = self.app.post('/users', data=json.dumps(
            {
                "name": "Tester",
                "salary": 9000
            }
        ), content_type='application/json')
        # HTTP status check
        self.assertEqual(result.status_code, 200)
        # Response data check
        self.assertTrue('id', result.data)
        self.__class__.test_id = json.loads(result.data)['id']

    # HTTP GET case: select all users
    def test_02_get_all(self):
        result = self.app.get('/users')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('id', result.data)
        self.assertTrue('name', result.data)
        self.assertTrue('salary', result.data)

    # HTTP GET case: select a user
    def test_03_get(self):
        result = self.app.get(
            '/users/%s' % str(self.__class__.test_id), method=['GET']
        )
        self.assertEqual(result.status_code, 200)
        self.assertTrue('id', result.data)
        self.assertTrue('name', result.data)
        self.assertTrue('salary', result.data)

    # HTTP PUT case: update a user
    def test_04_put(self):
        result = self.app.put(
            '/users/%s' % str(self.__class__.test_id),
            data=json.dumps({"name": "Updater", "salary": 0}),
            content_type='application/json'
        )
        self.assertEqual(result.status_code, 200)
        self.assertTrue('id', result.data)

    # HTTP DELETE case: delete a user
    def test_05_delete(self):
        result = self.app.delete(
            '/users/%s' % str(self.__class__.test_id), method=['DELETE']
        )
        self.assertEqual(result.status_code, 200)
        self.assertTrue('id', result.data)

    # Runs the unittest in the module.
    if __name__ == '__main__':
        unittest.main()
