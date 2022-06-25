""""
example unit test
"""

from . import tools

version = tools.import_command_module('version')

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
