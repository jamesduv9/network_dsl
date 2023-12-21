"""
Author: James Duvall
Module: routemap.py
Purpose: Generate all required routemap netconf edit-config rpc data
"""

from .compositeconfig import CompositeConfig
from .utilityconfig import UtilityConfig

class RouteMap(CompositeConfig, UtilityConfig):
    """
    RouteMap object
    Create and template rpc xml from template
    """

    def __init__(self, file_: dict, base_dir: str) -> None:
        super().__init__(file_=file_, base_dir=base_dir)
        self.pretemplate_data = self.parse_data("route_map")
        self.template = self.j2_env.get_template("rm_config.xml")
        self.xml_config = self.render_model_xml()
        self.model_validated = self.validate_model()

    def render_model_xml(self):
        """
        Render the configuration into the model's specific netconf config
        """
        return self.template.render(rm=self.pretemplate_data)

    def print_config(self) -> str:
        """
        Return edit-config rpc for specific module
        """
        rendered_data = self.edit_template.render(route_map=self.xml_config)
        return self.prettify_xml(rendered_data)
