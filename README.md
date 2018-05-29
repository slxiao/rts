# Introduction
RTS is for regression test selection. It's used for selecting only the affected regression tests based on file dependency. Specifically, only the tests that depend on the files that are changed in the current commit will be selected to execution. With RTS, testing resource is reduced and test feadback time is shortened, which benefits both developers and testers.

Different test automation projects using different programming languages would need different RTS techniques. The RTS technique presented here, named **rts**, is suitable for [Robot Framework](http://robotframework.org) based test automation projects. Robot Framework is a powerful [test automation framework]() widely used in the industry.

# Usage
Usage of **rts** is easy. Put `rts.py` to the path where the test execution command (in Robot Framework, this command is `pybot` or `rebot`) runs, and then execute the following command instead:
> python rts.py "your_pybot_command"

For example,

> python rts.py "pybot -L trace ."

> python rts.py "pybot -i status-regression -s 'test_suite_1' ."

# Development
**rts** is using TDD(Test-Driven Development). Use `make ut` to run all unit test cases.
> make ut

# Support
**rts** is developed and maintained by [slxiao](https://github.com/slxiao). Refer to [gitlab issues](https://github.com/slxiao/rts/issues) if you meet any bugs or need feature enhancements.

