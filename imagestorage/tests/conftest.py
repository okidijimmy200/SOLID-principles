def pytest_addoption(parser):
    parser.addoption(
        "--service", action="store", default="aws"
    )