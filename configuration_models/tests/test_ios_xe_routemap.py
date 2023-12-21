"""
Author: James Duvall
Module: test_ios_xe_routemap.py
Purpose: Basic testing for RouteMap object functionality
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


from ios_xe.routemap import RouteMap
from ios_xe.compositeconfig import CompositeConfig

#filepath to example yaml
example_yml_path = os.path.join(FILE_DIR, "example.yml")
#path to root directory
root_dir = FILE_DIR.parents[1]

@pytest.fixture
def routemap_object():
    config = RouteMap(file_=example_yml_path, base_dir=root_dir)
    return config

def test_is_instance_of_composite_config(routemap_object):
    assert isinstance(routemap_object, CompositeConfig)

def test_j2_env_is_instance_of_environment(routemap_object):
    assert isinstance(routemap_object.j2_env, Environment)

def test_config_is_dict(routemap_object):
    assert isinstance(routemap_object.config, dict)

def test_pretemplate_data_is_dict(routemap_object):
    assert isinstance(routemap_object.pretemplate_data, list)

def test_xml_is_valid(routemap_object):
    assert routemap_object.valid_xml_check(routemap_object.xml_config)
    assert routemap_object.valid_xml_check(routemap_object.print_config())

def test_prefixlist_data(routemap_object):
    assert '<route-map>' in routemap_object.xml_config
    assert '<route-map-seq xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-route-map" operation="replace">' in routemap_object.xml_config