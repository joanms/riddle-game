# The tests are based on this video: https://www.youtube.com/watch?v=1aHNs1aEATg&list=PLLjmbh6XPGK4ISY747FUHXEl9lBxre4mM&index=8&t=0s
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

          # Ensure that the first riddle displays after login
          def test_correct_login(self):
                    tester = app.test_client(self)
                    response = tester.post('/', data=dict(username="player1"), 
                    follow_redirects=True)
                    self.assertIn(b'Never resting, never still.', response.data)

          # Ensure the leaderboard page loads correctly
          def test_leaderboard_display(self):
                    tester = app.test_client(self)
                    response = tester.get('/leaderboard', follow_redirects=True)
                    self.assertIn(b'Leaderboard', response.data)
          
if  __name__ == '__main__':
          unittest.main()