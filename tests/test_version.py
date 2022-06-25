""""
example unit test
"""

import pytest
from . import tools

version = tools.import_command_module('version')

@pytest.fixture(scope="function")
def version_file_path(tmpdir_factory):
    """fixture version file"""
    return tmpdir_factory.mktemp("workit").join('version.txt')

@pytest.fixture(scope="function")
def version_file(version_file_path):  # pylint: disable = redefined-outer-name
    """fixture version file"""
    return tools.create_file(version_file_path, '1.2.3')

@pytest.fixture(scope="function")
def setupcfg_file_path(tmpdir_factory):
    """fixture setup.cfg file"""
    return tmpdir_factory.mktemp("workit").join('setup.cfg')

@pytest.fixture(scope="function")
def setupcfg_file(setupcfg_file_path):  # pylint: disable = redefined-outer-name
    """fixture setup.cfg file"""
    return tools.create_file(setupcfg_file_path, '[metadata]\nversion = 1.2.3')

class TestVersion():  # pylint: disable = too-few-public-methods
    """example test"""
    def test_get_version(self):  # pylint: disable = redefined-outer-name
        """test get_version"""
        assert version.get_version('1.2.3') == (1, 2, 3)

    def test_increment_version(self):  # pylint: disable = redefined-outer-name
        """test increment_version"""
        assert version.increment_version(1, 2, 3, 'patch') == (1, 2, 4)
        assert version.increment_version(1, 2, 3, 'minor') == (1, 3, 0)
        assert version.increment_version(1, 2, 3, 'major') == (2, 0, 0)

    def check_main(self, version_file_fixture, setupcfg_file_fixture, mode, expected_version):
        """check main result"""
        version.VERSION_PATH = str(version_file_fixture[0])
        version.SETUP_CFG_PATH = str(setupcfg_file_fixture[0])

        print('checking main:', version_file_fixture[1], '->', expected_version)
        version.main(mode)
        assert version.VERSION_PATH == str(version_file_fixture[0])
        assert version.SETUP_CFG_PATH == str(setupcfg_file_fixture[0])
        assert tools.load_file(str(version_file_fixture[0])) == expected_version
        assert tools.load_file(str(setupcfg_file_fixture[0])) \
            == f"[metadata]\nversion = {expected_version}"

    @pytest.mark.usefixtures('version_file', 'setupcfg_file')
    def test_main_patch(self, version_file, setupcfg_file):  # pylint: disable = redefined-outer-name
        """test main patch"""
        # 1.2.3 -> 1.2.4
        self.check_main(version_file, setupcfg_file, "patch", '1.2.4')

    @pytest.mark.usefixtures('version_file', 'setupcfg_file')
    def test_main_minor(self, version_file, setupcfg_file):  # pylint: disable = redefined-outer-name
        """test main minor"""
        # 1.2.3 -> 1.3.0
        self.check_main(version_file, setupcfg_file, "minor", '1.3.0')

    @pytest.mark.usefixtures('version_file', 'setupcfg_file')
    def test_main_major(self, version_file, setupcfg_file):  # pylint: disable = redefined-outer-name
        """test main major"""
        # 1.2.3 -> 2.0.0
        self.check_main(version_file, setupcfg_file, "major", '2.0.0')
