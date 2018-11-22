from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

          # Ensure that Flask was set up correctly
          def test_index(self):
                    tester = app.test_client(self)
                    response = tester.get('/', content_type='html/text')
                    self.assertEqual(response.status_code, 200)
          
          # Ensure that main page requires user login
          def test_main_route_requires_login(self):
                    tester = app.test_client(self)
                    response = tester.get('/', follow_redirects=True)
                    self.assertIn(b'Please select a username', response.data)

          # Ensure the leaderboard page loads
          def test_riddles_display(self):
                    tester = app.test_client(self)
                    response = tester.get('/leaderboard', follow_redirects=True)
                    self.assertEqual(response.status_code, 200)
          
if  __name__ == '__main__':
          unittest.main()