"""
Author: James Duvall
Module: prefixlist.py
Purpose: Generate all required prefix-lists netconf edit-config rpc data
"""

from .compositeconfig import CompositeConfig
from .utilityconfig import UtilityConfig

class PrefixList(CompositeConfig, UtilityConfig):
    """
    PrefixList object
    Create and template rpc xml from template
    """

    def __init__(self, file_: dict, base_dir: str) -> None:
        super().__init__(file_=file_, base_dir=base_dir)
        self.pretemplate_data = self.parse_data("prefix_list")
        self.template = self.j2_env.get_template("pl_config.xml")
        self.xml_config = self.render_model_xml()
        self.model_validated = self.validate_model()

    def render_model_xml(self):
        """
        Render the configuration into the model's specific netconf config
        """
        return self.template.render(pl=self.pretemplate_data)

    def print_config(self) -> str:
        """
        Return edit-config rpc for specific module
        """
        rendered_data = self.edit_template.render(prefix_list=self.xml_config)
        return self.prettify_xml(rendered_data)
