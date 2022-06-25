""""
example unit test
"""

from . import tools

version = tools.import_command_module('version')

class TestVersion():  # pylint: disable = too-few-public-methods
    """example test"""
    def test_get_version(self):  # pylint: disable = redefined-outer-name
        """test get_version"""
        assert version.get_version('1.2.3') == [1, 2, 3]
