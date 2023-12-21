import os
import subprocess
import logging
import xmltodict
import yaml
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from xml.dom.minidom import parseString
from jinja2 import Environment, FileSystemLoader


logger = logging.getLogger(__name__)


class UtilityConfig:
    """
    Helper methods to extend config classes
    """

    def parse_data(self, key_):
        try:
            return self.config.get("device").get(key_)
        except KeyError:
            logging.error(f"KeyError when fetching key - {key_} from self.config")

    def validate_model(self) -> bool:
        """
        Tests input yaml vs verified yang model
        """

        # Reusing some methods from my pytest modules
        device_data = self.load_and_parse_yaml(directory=".", yaml_file=self.file_)
        testable_xml = self.create_testable_xml(device_data=device_data)

        temp_xml_path = os.path.join(self.base_dir, "yang/test_device.xml")
        self.create_temp_xml(testable_xml, temp_xml_path)

        p = subprocess.run(
            [
                "yang2dsdl",
                "-v",
                temp_xml_path,
                os.path.join(self.base_dir, "yang/device_validator.yang"),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.join(self.base_dir, "yang"),
        )

        try:
            assert p.returncode == 0
        except AssertionError:
            logger.critical(f"Failed to validate the model \n {p.stderr}")
            exit(1)
        logger.info("YANG Model Validated correctly")
        return True

    def create_jinja_environment(self) -> Environment:
        """
        Creates a jinja2 environment for the templates directory
        """
        j2_dir = os.path.join(self.base_dir, "templates/ios_xe")
        return Environment(
            loader=FileSystemLoader(j2_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    @staticmethod
    def prettify_xml(xml_string: str) -> str:
        """
        Takes an XML string and returns a pretty version of it with proper indentation
        """
        try:
            dom = parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent="  ")
            return "\n".join(
                [
                    line
                    for line in pretty_xml.split("\n")
                    if line.strip() and line != '<?xml version="1.0" ?>'
                ]
            )
        except Exception as e:
            logging.critical(f"Error processing XML: {e}")
            return False

    @staticmethod
    def create_testable_xml(device_data: str) -> str:
        """
        yang2dsdl expects the xml input to be wrapped in the netconf namespace

        """

        return f"""<?xml version="1.0" encoding="utf-8"?>
        <data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        {device_data}
        </data>
        """

    @staticmethod
    def load_and_parse_yaml(directory: str, yaml_file: str) -> str:
        """
        Input a yaml file, and get back xml of the file
        """

        with open(os.path.join(directory, yaml_file), "r") as file:
            device_data = yaml.safe_load(file.read())
        device_data = xmltodict.unparse(
            device_data, full_document=False
        )  # False ensures it doesn't add xml tag
        return device_data

    @staticmethod
    def create_temp_xml(configuration: str, temp_file_path: str) -> None:
        """
        Creates an XML file that can be used for the yang2dsdl validation
        """

        with open(temp_file_path, "w") as file:
            file.write(configuration)

    @staticmethod
    def valid_xml_check(xml_string):
        try:
            ET.fromstring(xml_string)
            return True
        except ParseError:
            return False