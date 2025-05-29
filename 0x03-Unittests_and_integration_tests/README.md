# 0x03-Unittests and Integration Tests

## **Project Overview**
This project focuses on **unit testing** and **integration testing** in Python, using the `unittest` module, `mocking`, and `parameterized` testing techniques. We thoroughly tested the `GithubOrgClient` class to ensure its methods work correctly without making real API calls.

---

## **Tasks and Implementation**

### **Task 0: Parameterize a Unit Test**
- Used `@parameterized.expand` to **test `access_nested_map`** with multiple input cases.
- Verified that the function correctly retrieves nested values.
- Ensured a **KeyError** is raised when accessing non-existing keys.

### **Task 1: Mock HTTP Calls**
- Tested `get_json(url)` while **mocking HTTP responses** using `requests.get`.
- Used `@patch` to replace real API calls with mock data.
- Ensured the function correctly retrieved payloads from different URLs.

### **Task 2: Parameterize & Patch**
- Unit-tested `GithubOrgClient.org` using **mocked API responses**.
- Parameterized tests for different organization names.
- Checked whether `get_json` is **called exactly once** with the correct URL.

### **Task 3: Memoization**
- Ensured the `@memoize` decorator prevents duplicate API calls.
- Used `mock` to verify that a method is **called only once** even when accessed multiple times.

### **Task 4: Patching as Decorators**
- Tested `GithubOrgClient.org` while **patching `get_json` directly**.
- Used decorators to apply mocks efficiently.
- Confirmed that memoization does not cause redundant API calls.

### **Task 5: Mocking a Property**
- Mocked the `GithubOrgClient.org` method using `PropertyMock`.
- Ensured the `repos` property correctly extracts the `repos_url`.
- Verified that `org` was **called only once**.

### **Task 6: More Patching**
- Unit-tested `GithubOrgClient.public_repos`.
- Used `@patch` to **mock both `get_json` and `_public_repos_url`**.
- Verified the list of repositories **matches expected output**.
- Ensured mocked functions were **called exactly once**.

### **Task 7: Parameterized `has_license`**
- Parameterized tests for `GithubOrgClient.has_license`.
- Used different repo structures and license keys to validate correctness.
- Ensured the method properly extracts licenses **or returns False**.

### **Task 8: Integration Test (Fixtures)**
- **Mocked external requests** using `patch("requests.get")`.
- Used `@parameterized_class` to apply data from `fixtures.py`.
- Ensured that `GithubOrgClient.public_repos` correctly integrates **API responses**.
- Validated expected repositories against fixture data.

---

## **How to Run the Tests**
Execute the tests using:
```bash
python test_utils.py
python test_client.py
```
For a detailed test output, use the verbose mode option:
```bash
python test_utils.py -v
python test_client.py -v
```