import os
import yaml
import xmltodict
import pytest
import subprocess


yang_dir = os.path.dirname(os.path.abspath(f"{__file__}/../"))

def create_testable_xml(device_data: str) -> str:

    """
    yang2dsdl expects the xml input to be wrapped in the netconf namespace

    """

    return f"""<?xml version="1.0" encoding="utf-8"?>
    <data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    {device_data}
    </data>
    """

def load_and_parse_yaml(directory:str, yaml_file: str) -> str:
    """
    Input a yaml file, and get back xml of the file
    """

    with open(os.path.join(directory, yaml_file), "r") as file:
        device_data = yaml.safe_load(file.read())
    device_data = xmltodict.unparse(device_data, full_document=False) #False ensures it doesn't add xml tag
    return device_data

def create_temp_xml(configuration: str, temp_file_path: str) -> None:
    """
    Creates an XML file that can be used for the yang2dsdl validation
    """

    with open(temp_file_path, "w") as file:
        file.write(configuration)

@pytest.fixture()
def process_check(request):
    """
    Creates a yang2dsdl compatible xml document from a yaml file, then run the yang2dsdl test
    as a subprocess, return it to the test function for exit_code checks
    """

    device_data = load_and_parse_yaml(directory=os.path.join(yang_dir, request.param[0]), yaml_file=request.param[1])
    testable_xml = create_testable_xml(device_data=device_data)
    
    temp_xml_path = os.path.join(yang_dir, "test_device.xml")
    create_temp_xml(testable_xml, temp_xml_path)

    p = subprocess.run(["yang2dsdl", "-v", temp_xml_path, os.path.join(yang_dir, "device_validator.yang")], 
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=yang_dir)
    return p, request.param[1]
