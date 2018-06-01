import unittest
from rts import RTS

class TestRTS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rts = RTS(".", [])

    def test_get_dependency(self):
        self.rts.root = './testdata'
        self.assertNotEqual(self.rts.generate_dependency(), {})

    def test_select_suites(self):
        self.rts.dependency = {"ET":["NbsLibrary", "common_lib"]}
        self.assertEqual(self.rts.select_suites(["common_lib"]), ["ET"])
        self.rts.dependency = {"ET":["NbsLibrary", "common_lib2"]}
        self.assertEqual(self.rts.select_suites(["common_lib"]), [])

    def test_get_dryrun_cmd(self):
        self.rts.root = "/home/user"
        self.rts.suites = ["suite1", "suite2"]
        self.assertEqual(self.rts.get_dryrun_cmd(), 'cd /home/user && pybot --dryrun -s suite1 -s suite2 .')

if __name__ == '__main__':
    unittest.main()
