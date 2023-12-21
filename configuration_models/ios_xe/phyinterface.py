"""
Author: James Duvall
Module: phyinterfaceconfig.py
Purpose: Generate all required phyinterfaceconfig netconf edit-config rpc data
"""

from .compositeconfig import CompositeConfig
from .utilityconfig import UtilityConfig

class PhyInterface(CompositeConfig, UtilityConfig):
    """
    Physical interface object
    Create and template rpc xml from template
    """

    def __init__(self, file_: dict, base_dir: str) -> None:
        super().__init__(file_=file_, base_dir=base_dir)
        self.pretemplate_data = self.parse_data("interface").get("physical_interfaces")
        self.interface_parse()
        self.template = self.j2_env.get_template("physical_interface_config.xml")
        self.xml_config = self.render_model_xml()
        self.model_validated = self.validate_model()
        

    def render_model_xml(self):
        """
        Render the configuration into the model's specific netconf config
        """
        return self.template.render(physical_interfaces=self.pretemplate_data)

    def print_config(self) -> str:
        """
        Return edit-config rpc for specific module
        """
        rendered_data = self.edit_template.render(physical_interfaces=self.xml_config)
        return self.prettify_xml(rendered_data)
    
    def interface_parse(self):
        """
        Parses the user's interface name and includes specific needed values
        """
        for interface in self.pretemplate_data:
            current_interface = interface.get("name")
            interface["base_interface"] = current_interface.split("Ethernet")[0] + "Ethernet"
            interface["identifier"] = current_interface.split(interface['base_interface'])[1]
