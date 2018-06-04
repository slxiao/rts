import subprocess
import re
from robot.api import ExecutionResult, ResultVisitor
import sys

SUPPORT_FILE_TYPES = ["robot", "py"]

def get_changed_files(cmd="git diff HEAD HEAD~ --name-only"):
    return subprocess.check_output(cmd, shell=True).strip().split('\n')

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
    def __init__(self, root, directory, suites):
        self.root = root
        self.directory = directory
        self.suites = suites
        self.dependency = {}
        print "suite path: %s, suites: %s." % (root, str(suites))

    def select(self, changes):
        print "file changes: %s." % changes
        print "precheck changes."
        if not self.precheck_changes(changes):
            print "unsupported file changes, no selection."
            return self.suites
        self.dryrun()
        print "compute dependency mappings."
        self.generate_dependency()
        print "select suites based on dependency."
        return self.select_suites(changes)

    def precheck_changes(self, changes):
        for change in changes:
            if not change.startswith(self.root) or change.split(".")[-1] not in SUPPORT_FILE_TYPES:
                return False
        return True

    def dryrun(self):
        cmd = self.get_dryrun_cmd()
        print cmd
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        if out:
            print out

    def get_dryrun_cmd(self):
        suites=["'%s'" % s for s in self.suites]
        return "pybot --dryrun " + " ".join([ "-s "+s for s in suites]) + " %s" % self.directory

    def generate_dependency(self):
        output = "./output.xml"
        result = ExecutionResult(output)
        visitor = FileDependencyVisitor()
        result.visit(visitor)
        self.dependency = visitor.dependency

    def select_suites(self, changes):
        selected = []
        changes = [x.split("/")[-1].split(".")[0] for x in changes]
        for suite in self.dependency:
            if set(self.dependency[suite]).intersection(changes):
                selected.append(suite)
        return selected

if __name__ == "__main__":
    print sys.argv
    root = sys.argv[1]
    directory = sys.argv[2]
    suites = eval(sys.argv[3])
    changes = eval(sys.argv[4])
    print RTS(root, directory, suites).select(changes)
