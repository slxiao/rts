import unittest
from rts import RTS

class TestRTS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rts = RTS()

    def test_get_output_path(self):
        cmd = "pybot -d ./log -o o.xml ."
        self.assertEqual(self.rts._get_output_path(cmd), "./log/o.xml")

if __name__ == '__main__':
    unittest.main()
