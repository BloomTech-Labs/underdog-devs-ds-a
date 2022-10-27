# Unit Testing Framework

---
### Running Tests
- To run a single test suite file, run it directly from the IDE or from the terminal as a python module with `python -m <test_filename.py>` Some test suites may have to be run in a different working directory than the unit_tests folder; consult your IDE docs to set up the proper runtime environment.
- All unit tests can be automatically run from the `run_tests` shell script in the root directory. Note that only properly named tests will be run from the automatic discovery process.

---
### Organization
- Each module to be tested should have its tests in a separate file in the  `/tests/unit_tests` folder named `test_<app subfolder name><module name>.py` (eg. `/tests/unit_tests/test_app_data.py`)
- Each unittest test suite class should be named `Test<ClassName>` or `Test<FunctionName>` and each test method should be named `test_<tested_function>_<test_details>`. Choose whatever structure makes the most sense for the specific file being tested.
- For ease of later reference, keep test suites in roughly the same order as the functions they test appear in the original files.

---
### Format Guidelines
- Each tests file should have a `if __name__ == '__main__':` section at the end which calls `unittest.main()` to allow each test file to be run individually from the terminal or IDE. The `verbosity` parameter in `unittest.main(...)` should be set to `2` during most testing.
- Use the `setUp()` and `tearDown()` inherited methods (and their variants `setUpClass()` / `tearDownClass()`) to re-use setup code for individual tests and whole test suites, respectively.
- Use the `mock` module under `unittest` to isolate the function/method under test from its dependencies by rerouting calls to outside resources to `Mock` objects with pre-set return values. Alternatively, or in concert with `mock`, use the `patch` submodule's decorator to intercept a specific function call during a single test method with a return value specified locally in the test method.