""""
example unit test
"""

import json
import os
import pytest
from . import tools

bootstrap = tools.import_command_module('bootstrap')

@pytest.fixture(scope="function")
def template_file_path(tmpdir_factory):
    """fixture template file"""
    return tmpdir_factory.mktemp("workit").join('template.txt')

@pytest.fixture(scope="function")
def template_file(template_file_path):  # pylint: disable = redefined-outer-name
    """fixture template file"""
    return tools.create_file(template_file_path, '${foo}${bar}')

@pytest.fixture(scope="function")
def user_data_data():
    """fixture user data data"""
    return dict(
        developer_fullname='Foobar',
        developer_email='foobar@local.lan',
        developer_login='foobar'
    )

@pytest.fixture(scope="function")
def user_data_file_path(tmpdir_factory):
    """fixture user data file"""
    return tmpdir_factory.mktemp("workit").join('ppm.json')

@pytest.fixture(scope="function")
def user_data_file(user_data_file_path, user_data_data):  # pylint: disable = redefined-outer-name
    """fixture user data file"""
    return tools.create_file(
        user_data_file_path,
        json.dumps(user_data_data, indent=4)
    )

class TestBootstrapTools():  # pylint: disable = too-few-public-methods
    """bootstrap tools test"""
    @pytest.mark.usefixtures('template_file')
    def test_substitute_file(self, template_file):  # pylint: disable = redefined-outer-name
        """test substitute_file"""
        bootstrap.substitute_file(str(template_file[0]), {'foo': 'FOO', 'bar': 'BAR'})
        assert tools.load_file(str(template_file[0])) == 'FOOBAR'


class TestBootstrapController():  # pylint: disable = too-few-public-methods
    """bootstrap controller test"""
    def test_init(self):  # pylint: disable = redefined-outer-name
        """test init"""
        ctl = bootstrap.PpmBootstrapController()
        assert isinstance(ctl.user_data, dict)
        assert isinstance(ctl.data, dict)

    @pytest.mark.usefixtures('user_data_file', 'user_data_data')
    def test_load_user_data(self, user_data_file, user_data_data):  # pylint: disable = redefined-outer-name
        """test load_user_data"""
        bootstrap.USER_DATA_FILE = str(user_data_file[0])
        ctl = bootstrap.PpmBootstrapController()
        ctl.load_user_data()
        assert ctl.user_data == user_data_data

    @pytest.mark.usefixtures('user_data_file', 'user_data_data')
    def test_save_user_data(self, user_data_file, user_data_data):  # pylint: disable = redefined-outer-name
        """test load_user_data"""
        bootstrap.USER_DATA_FILE = str(user_data_file[0])
        ctl = bootstrap.PpmBootstrapController()
        ctl.data = user_data_data
        ctl.save_user_data()
        assert os.path.exists(user_data_file[0]) \
            and json.loads(tools.load_file(str(user_data_file[0]))) == user_data_data

    def test_check_files_raise_dir_missing(self):
        """test check_files: dir missing"""
        bootstrap.DIRS = ['/idonotexist']
        bootstrap.FILES = []
        ctl = bootstrap.PpmBootstrapController()
        with pytest.raises(bootstrap.PpmBootstrapException):
            ctl.check_files()

    def test_check_files_dir_exist(self):
        """test check_files: dir exists"""
        bootstrap.DIRS = ['/tmp']
        bootstrap.FILES = []
        ctl = bootstrap.PpmBootstrapController()
        try:
            ctl.check_files()
        except bootstrap.PpmBootstrapException as exception:
            assert False, f'{exception} should not raise'

    def test_check_files_raise_file_missing(self):
        """test check_files: file missing"""
        bootstrap.DIRS = []
        bootstrap.FILES = ['/idonotexist.txt']
        ctl = bootstrap.PpmBootstrapController()
        with pytest.raises(bootstrap.PpmBootstrapException):
            ctl.check_files()

    @pytest.mark.usefixtures('template_file')
    def test_check_files_file_exist(self, template_file):  # pylint: disable = redefined-outer-name
        """test check_files: file exists"""
        bootstrap.DIRS = []
        bootstrap.FILES = [str(template_file[0])]
        ctl = bootstrap.PpmBootstrapController()
        try:
            ctl.check_files()
        except bootstrap.PpmBootstrapException as exception:
            assert False, f'{exception} should not raise'
