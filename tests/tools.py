"""test tools"""

import os
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

def import_command_module(command_name):
    """import ppm command module"""
    # command file name is the command name
    # (without .py due to python shebang inside command script)
    command_file_name = command_name
    spec = spec_from_loader(
        command_name,
        SourceFileLoader(command_name, os.path.join(os.getcwd(), 'bin', command_file_name))
    )
    command_module = module_from_spec(spec)
    spec.loader.exec_module(command_module)

    return command_module

def create_file(func, content):
    """
    create test file
    @return (func, file_desc, content, )
    """
    with open(str(func), "w", encoding='utf-8') as file_desc:
        file_desc.write(content)
        return (func, content, file_desc)

def load_file(file_path):
    """load file"""
    with open(file_path, "r", encoding='utf-8') as file_desc:
        return file_desc.read()
