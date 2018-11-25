# Introduction
RTS is for regression test selection. It's used for selecting only the affected regression tests based on file dependency. Specifically, only the tests that depend on the files that are changed in the current commit will be selected to execution. With RTS, testing resource is reduced and test feadback time is shortened, which benefits both developers and testers.

Different test automation projects using different programming languages would need different RTS techniques. The RTS technique presented here, named **rts**, is suitable for [Robot Framework](http://robotframework.org) based test automation projects. Robot Framework is a powerful [test automation framework]() widely used in the industry.

# Usage
There are two ways to use **rts**.

First way is in Python, where you can:
```python
from rts import RTS

print RTS(".", ".", ["suite1", "suite2"]).select(["x.robot", "y.py"])

```
Example output might be
```python
["suite1"] #selected suites are printed. only suite1 depends on x.robot or y.py. suite2 not depend on any of the changes.
```
Second way is in Shell, where you can:
```shell
python rts.py . . '["suite1", "suite1"]' '["x.robot", "y.py"]'

```
Example output is same as above.

Note:
 - **rts** only supports `.robot` and `.py` files. **rts** supports dependency between two robot files, and dependency between a robot file and a python file. However, it does not detect dependency between two python files.
 - **rts** can detect suite-level dependency. It cannot detect case-level dependency or keyword-level dependency.
# Development
**rts** is using TDD(Test-Driven Development). Use `make ut` to run all unit test cases.
> make ut

# Support
**rts** is developed and maintained by [slxiao](https://github.com/slxiao). Refer to [gitlab issues](https://github.com/slxiao/rts/issues) if you meet any bugs or need feature enhancements.
