import subprocess
import re

class RTS(object):
    def __init__(self):
        pass

    def dryrun(self, cmd):
        cmd = cmd[0:6] + "--dryrun " + cmd[6:]
        try:
            subprocess.check_output(cmd, shell=True)
        except:
            raise RuntimeError("Dryrun failed, please check test cases!")

    def _get_output_path(self, cmd):
        directory = re.search("-d\s\S*", cmd)
        name = re.search("-o\s\S*", cmd)
        if directory:
            directory = directory.group(0).split(" ")[-1]
        else:
            directory = '.'
        if name:
            name = name.group(0).split(" ")[-1]
        else:
            name = "output.xml"
        return directory + '/' + name

    def get_dependency(self, output):
        dependency = {}
        return dependency

