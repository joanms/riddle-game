import unittest
import run

class TestStringMethods(unittest.TestCase):
          
          def test_start(self):
                    session = run.start()
                    score = session['score']
                    riddle_number = session['riddle_number']
                    attempt = session['riddle_attempt']
                    self.assertEqual(score, 0)
                    self.assertEqual(riddle_number, 0)
                    self.assertEqual(attempt, 1)
