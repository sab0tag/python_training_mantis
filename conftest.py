import pytest
import json
import os.path
from fixture.application import Application

fixture = None
target = None


def loadconfig(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


# fixture init
@pytest.fixture
def app(request):
    global fixture  # define global variable inside of the method
    browser = request.config.getoption("--browser")
    webconfig = loadconfig(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=webconfig['baseUrl'])  # constructor application
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()
    # destroy fixture
    request.addfinalizer(fin)
    return fixture

@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")

# add additional parameters inside of function; called once at the beginning ot the test run
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")  # where action will be automatically true if flag is present;

