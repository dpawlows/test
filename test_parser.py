import unittest
from parser import parse_input

class TestParser(unittest.TestCase):
    def test_parse_time_and_boundary(self):
        data = parse_input('input.ozone')
        self.assertIn('TIME', data)
        self.assertEqual(data['TIME'], [7, 12.0])
        self.assertIn('TOPBOUNDARY', data)
        self.assertEqual(data['TOPBOUNDARY'], [100])

if __name__ == '__main__':
    unittest.main()
