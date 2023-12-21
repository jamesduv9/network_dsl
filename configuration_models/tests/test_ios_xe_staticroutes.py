"""
Author: James Duvall
Module: test_ios_xe_staticroutes.py
Purpose: Basic testing for StaticRoute object functionality
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

from ios_xe.staticroutes import StaticRoutes
from ios_xe.compositeconfig import CompositeConfig

#filepath to example yaml
example_yml_path = os.path.join(FILE_DIR, "example.yml")
#path to root directory
root_dir = FILE_DIR.parents[1]

@pytest.fixture
def staticroute_object():
    config = StaticRoutes(file_=example_yml_path, base_dir=root_dir)
    return config

def test_is_instance_of_composite_config(staticroute_object):
    assert isinstance(staticroute_object, CompositeConfig)

def test_j2_env_is_instance_of_environment(staticroute_object):
    assert isinstance(staticroute_object.j2_env, Environment)

def test_config_is_dict(staticroute_object):
    assert isinstance(staticroute_object.config, dict)

def test_pretemplate_data_is_dict(staticroute_object):
    assert isinstance(staticroute_object.pretemplate_data, dict)

def test_vrf_dict_is_dict(staticroute_object):
    assert isinstance(staticroute_object.vrf_dict, dict)

def test_vrf_dict_contains_mgmt(staticroute_object):
    assert "mgmt" in staticroute_object.vrf_dict.keys()

def test_vrf_dict_contains_test(staticroute_object):
    assert "test" in staticroute_object.vrf_dict.keys()

def test_vrf_dict_mgmt_length(staticroute_object):
    assert len(staticroute_object.vrf_dict["mgmt"]) > 1

def test_vrf_dict_no_global(staticroute_object):
    assert "global" not in staticroute_object.vrf_dict.keys()

def test_pretemplate_data_keys(staticroute_object):
    assert "vrf" in staticroute_object.pretemplate_data.keys()
    assert "global" in staticroute_object.pretemplate_data.keys()

def test_xml_is_valid(staticroute_object):
    assert staticroute_object.valid_xml_check(staticroute_object.xml_config)
    assert staticroute_object.valid_xml_check(staticroute_object.print_config())

def test_prefixlist_data(staticroute_object):
    assert '<route operation="replace">' in staticroute_object.xml_config
    assert '<ip-route-interface-forwarding-list>' in staticroute_object.xml_config