import subprocess
import re
from robot.api import ExecutionResult, ResultVisitor
import sys

SUPPORT_FILE_TYPES = ["robot", "py"]

class FileDependencyVisitor(ResultVisitor):
    def __init__(self):
        self.dependency = {}

    def visit_suite(self, suite):
        suites = self.get_suites(suite)
        suites.remove(suite)
        for suite in suites:
            self.dependency[suite.name] = self.get_invoked_libraries(suite)
            self.dependency[suite.name].append(suite.name.replace(" ", "_"))

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
    def select(self, cmd):
        self.dryrun(cmd)
        output = self._get_output_path(cmd)
        print "compute dependency mapping."
        dependency = self.get_dependency(output)
        supported, changes = self.get_changed_files()
        print "compute changed files: %s." % str(changes)
        if not supported:
            print "no supported changes, no selection, return raw command."
            return [], cmd
        print "compute selected test suites."
        selected_suites = self.get_selected_suites(dependency, changes)
        cmd = self.get_updated_cmd(cmd, selected_suites)
        print "selected suites are %s, updated command is %s" % (str(selected_suites), cmd)
        return selected_suites, cmd

    def get_updated_cmd(self, cmd, suites):
        if not suites:
            return cmd
        origin_suites = re.findall("-s\s\S*", cmd)
        for s in origin_suites:
            cmd = cmd.replace(s, "")
        append = ""
        for s in suites:
            append += " -s '%s' " % s
        return re.sub(' +',' ', cmd[0:6] + append + cmd[6:])

    def dryrun(self, cmd):
        cmd = [cmd[0:6] + "--dryrun " + cmd[6:]]
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        if out:
            print out

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
        for f in result:
            if f.split(".")[-1] not in SUPPORT_FILE_TYPES:
                return False, None
        return True, [f.split('/')[-1].split(".")[0] for f in result]

    def get_selected_suites(self, dependency, changes):
        res = []
        for suite in dependency:
            if set(dependency[suite]).intersection(changes):
                res.append(suite)
        return res

if __name__ == "__main__":
    rts = RTS()
    rts.select(sys.argv[1])
