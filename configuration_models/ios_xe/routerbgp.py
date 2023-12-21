"""
Author: James Duvall
Module: routerbgp.py
Purpose: Generate all required router bgp netconf edit-config rpc data
"""

from .compositeconfig import CompositeConfig
from .utilityconfig import UtilityConfig

class RouterBgp(CompositeConfig, UtilityConfig):
    """
    RouterBgp object
    Create and template rpc xml from template
    """

    def __init__(self, file_: dict, base_dir: str) -> None:
        super().__init__(file_=file_, base_dir=base_dir)
        self.pretemplate_data = self.parse_data("router_bgp")
        self.template = self.j2_env.get_template("bgp_config.xml")
        self.xml_config = self.render_model_xml()
        self.model_validated = self.validate_model()

    def render_model_xml(self):
        """
        Render the configuration into the model's specific netconf config
        """
        #Template expect unpacked data
        return self.template.render(**self.pretemplate_data)

    def print_config(self) -> str:
        """
        Return edit-config rpc for specific module
        """
        rendered_data = self.edit_template.render(bgp=self.xml_config)
        return self.prettify_xml(rendered_data)
