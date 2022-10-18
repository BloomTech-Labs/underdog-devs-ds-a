# Unit Testing Framework

---
### Organization
- Each module to be tested should have its tests in a separate file in the  `/tests/unit_tests` folder named `test_<app subfolder name><module name>.py` (eg. `/tests/unit_tests/test_routers_data.py`)
- For consistency, each test suite class should be named `Test<ClassName>` or `Test<FunctionName>` and each test method should be named `test_<method>_<details>` or `test_<function>_<details>` respectively, depending on the structure of the module being tested.
- For ease of later reference, try to keep test suites in roughly the same order as the functions they test appear in the original files.
---
### Format Guidelines
- Each tests file should have a `if __name__ == '__main__':` section at the end which calls `unittest.main()` to allow each test file to be run individually from the terminal or IDE. Optionally the `verbosity` argument can be specified in `unittest.main(...)`  to the desired level of test output for that file.
- Use the `setUp()` and `tearDown()` inherited methods (and their variants) to re-use setup code for individual tests
- Use the `Mock()` class operators and/or the `@patch` decorator to isolate the function/method under test from its dependencies as much as possible. Especially important is to isolate out actual database calls, as these are time-consuming to resolve during a test suite. 