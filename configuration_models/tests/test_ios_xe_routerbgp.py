"""
Author: James Duvall
Module: test_ios_xe_routerbgp.py
Purpose: Basic testing for RouterBgp object functionality
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


from ios_xe.routerbgp import RouterBgp
from ios_xe.compositeconfig import CompositeConfig

#filepath to example yaml
example_yml_path = os.path.join(FILE_DIR, "example.yml")
#path to root directory
root_dir = FILE_DIR.parents[1]

@pytest.fixture
def routerbgp_object():
    config = RouterBgp(file_=example_yml_path, base_dir=root_dir)
    return config

def test_is_instance_of_composite_config(routerbgp_object):
    assert isinstance(routerbgp_object, CompositeConfig)

def test_j2_env_is_instance_of_environment(routerbgp_object):
    assert isinstance(routerbgp_object.j2_env, Environment)

def test_config_is_dict(routerbgp_object):
    assert isinstance(routerbgp_object.config, dict)

def test_pretemplate_data_is_dict(routerbgp_object):
    assert isinstance(routerbgp_object.pretemplate_data, dict)

def test_pretemplate_data_root_keys(routerbgp_object):
    assert "asn" in routerbgp_object.pretemplate_data.keys()
    assert "router_id" in routerbgp_object.pretemplate_data.keys()
    assert "peer_group" in routerbgp_object.pretemplate_data.keys()
    assert "neighbor" in routerbgp_object.pretemplate_data.keys()
    assert "address_family" in routerbgp_object.pretemplate_data.keys()

def test_xml_is_valid(routerbgp_object):
    assert routerbgp_object.valid_xml_check(routerbgp_object.xml_config)
    assert routerbgp_object.valid_xml_check(routerbgp_object.print_config())

def test_prefixlist_data(routerbgp_object):
    assert '<bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp" operation="replace">' in routerbgp_object.xml_config
    assert '<neighbor>' in routerbgp_object.xml_config