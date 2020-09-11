import pytest
import json
import os.path
from fixture.application import Application
import ftputil

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


@pytest.fixture(scope="session")
def config(request):
    return loadconfig(request.config.getoption("--target"))


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'],
                                 config['ftp']['username'],
                                 config['ftp']['password'])

    def fin():
        restore_server_configuration(config['ftp']['host'],
                                     config['ftp']['username'],
                                     config['ftp']['password'])

    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php", "config_inc.php"))


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc_php")
        remote.rename("config_inc.php.bak", "config_inc.php")
