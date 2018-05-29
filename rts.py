import subprocess
import re
from robot.api import ExecutionResult, ResultVisitor
import sys

class FileDependencyVisitor(ResultVisitor):
    def __init__(self):
        self.dependency = {}

    def visit_suite(self, suite):
        suites = self.get_suites(suite)
        for suite in suites:
            self.dependency[suite.name] = self.get_invoked_libraries(suite)

    def get_suites(self, suite):
        res = [suite]
        for s in suite.suites:
            res += self.get_suites(s)
        return res

    def get_invoked_libraries(self, model):
        keywords = self.get_invoked_keywords(model)
        res = []
        for kw in keywords:
            if '.' in kw.name and "{" not in kw.name:
                lib = kw.name.split(".")[0]
                if lib not in res:
                    res.append(lib)
        return res

    def get_invoked_keywords(self, model):
        res = [model]
        for kw in model.keywords:
            res += self.get_invoked_keywords(kw)
        if hasattr(model, "tests"):
            for test in model.tests:
                res += self.get_invoked_keywords(test)
        if hasattr(model, "suites"):
            for suite in model.suites:
                res += self.get_invoked_keywords(suite)
        return res

class RTS(object):
    def run(self, cmd):
        self.dryrun(cmd)
        output = self._get_output_path(cmd)
        dependency = self.get_dependency(output)
        changes = self.get_changed_files()
        affected = self.get_affected_suites(dependency, changes)
        cmd = self.get_updated_cmd(cmd, affected)
        subprocess.check_output(cmd, shell=True)

    def get_updated_cmd(self, cmd, suites):
        origin_suites = re.findall("-s\s\S*", cmd)
        for s in origin_suites:
            cmd = cmd.replace(s, "")
        append = ""
        for s in suites:
            append += "-s '%s'" % s
        return cmd[0:6] + append + cmd[6:]

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
        result = ExecutionResult(output)
        visitor = FileDependencyVisitor()
        result.visit(visitor)
        return visitor.dependency

    def get_changed_files(self, cmd="git diff HEAD HEAD~ --name-only"):
        result = subprocess.check_output(cmd, shell=True)
        result = result.strip().split('\n')
        return [name.split('/')[-1].split(".")[0] for name in result if name.startswith('test/ET')]

    def get_affected_suites(self, dependency, changes):
        res = {}
        for suite in dependency:
            if set(dependency[suite]).intersection(changes):
                res[suite] = True
            else:
                res[suite] = False
        return res

if __name__ == "__main__":
    rts = RTS()
    rts.run(sys.argv[1])
