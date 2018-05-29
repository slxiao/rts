import unittest
from rts import RTS

class TestRTS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rts = RTS()

    def test_get_output_path(self):
        cmd = "pybot -d ./log -o o.xml ."
        self.assertEqual(self.rts._get_output_path(cmd), "./log/o.xml")
        cmd = "pybot ."
        self.assertEqual(self.rts._get_output_path(cmd), "./output.xml")
        cmd = "pybot -o o.xml ."
        self.assertEqual(self.rts._get_output_path(cmd), "./o.xml")
        cmd = "pybot -d ./log ."
        self.assertEqual(self.rts._get_output_path(cmd), "./log/output.xml")

    def test_get_dependency(self):
        output = './testdata/output.xml'
        self.assertNotEqual(self.rts.get_dependency(output), {})

    def test_get_affected_suites(self):
        dependency = {"ET":["NbsLibrary", "common_lib"]}
        changes = ["common_lib"]
        self.assertEqual(self.rts.get_affected_suites(dependency, changes), {"ET":True})
        dependency = {"ET":["NbsLibrary", "common_lib2"]}
        changes = ["common_lib"]
        self.assertEqual(se lf.rts.get_affected_suites(dependency, changes), {"ET":False})

    def test_get_updated_cmd(self):
        cmd = "pybot -s 'FM' -s 'CM' ."
        suites = ["FM_2"]
        self.assertEqual(self.rts.get_updated_cmd(cmd, suites), "pybot -s 'FM_2'  .")

if __name__ == '__main__':
    unittest.main()
