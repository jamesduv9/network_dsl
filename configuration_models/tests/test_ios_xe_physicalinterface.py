"""
Author: James Duvall
Module: test_ios_xe_phyinterface.py
Purpose: Basic testing for PhyInterface object functionality
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


from ios_xe.phyinterface import PhyInterface
from ios_xe.compositeconfig import CompositeConfig

#filepath to example yaml
example_yml_path = os.path.join(FILE_DIR, "example.yml")
#path to root directory
root_dir = FILE_DIR.parents[1]

@pytest.fixture
def phyinterface_object():
    config = PhyInterface(file_=example_yml_path, base_dir=root_dir)
    return config

def test_is_instance_of_composite_config(phyinterface_object):
    assert isinstance(phyinterface_object, CompositeConfig)

def test_j2_env_is_instance_of_environment(phyinterface_object):
    assert isinstance(phyinterface_object.j2_env, Environment)

def test_config_is_dict(phyinterface_object):
    assert isinstance(phyinterface_object.config, dict)

def test_pretemplate_data_is_dict(phyinterface_object):
    assert isinstance(phyinterface_object.pretemplate_data, list)

def test_xml_is_valid(phyinterface_object):
    assert phyinterface_object.valid_xml_check(phyinterface_object.xml_config)
    assert phyinterface_object.valid_xml_check(phyinterface_object.print_config())

def test_prefixlist_data(phyinterface_object):
    assert '<name>' in phyinterface_object.xml_config