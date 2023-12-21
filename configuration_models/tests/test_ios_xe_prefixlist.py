"""
Author: James Duvall
Module: test_ios_xe_prefixlist.py
Purpose: Basic testing for PrefixList object functionality
Note: No docstrings for methods, detail is in the names
"""

import os
import sys
import pytest
from pathlib import Path
from jinja2 import Environment
FILE_DIR = Path(__file__).resolve().parent
path = os.path.dirname(FILE_DIR)
print(path)
sys.path.append(path)


from ios_xe.prefixlist import PrefixList
from ios_xe.compositeconfig import CompositeConfig

#filepath to example yaml
example_yml_path = os.path.join(FILE_DIR, "example.yml")
#path to root directory
root_dir = FILE_DIR.parents[1]

@pytest.fixture
def prefixlist_object():
    config = PrefixList(file_=example_yml_path, base_dir=root_dir)
    return config

def test_is_instance_of_composite_config(prefixlist_object):
    assert isinstance(prefixlist_object, CompositeConfig)

def test_j2_env_is_instance_of_environment(prefixlist_object):
    assert isinstance(prefixlist_object.j2_env, Environment)

def test_config_is_dict(prefixlist_object):
    assert isinstance(prefixlist_object.config, dict)

def test_pretemplate_data_is_dict(prefixlist_object):
    assert isinstance(prefixlist_object.pretemplate_data, list)

def test_xml_is_valid(prefixlist_object):
    assert prefixlist_object.valid_xml_check(prefixlist_object.xml_config)
    assert prefixlist_object.valid_xml_check(prefixlist_object.print_config())

def test_prefixlist_data(prefixlist_object):
    assert '<prefix-lists operation="replace">' in prefixlist_object.xml_config
    assert '<prefixes>' in prefixlist_object.xml_config
