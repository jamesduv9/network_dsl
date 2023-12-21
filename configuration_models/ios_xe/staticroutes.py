"""
Author: James Duvall
Module: staticroutes.py
Purpose: Creates all needed netconf edit-config rpc data needed
"""


from collections import defaultdict
from .compositeconfig import CompositeConfig
from .utilityconfig import UtilityConfig

class StaticRoutes(CompositeConfig, UtilityConfig):
    """
    Static routes class, responsible for templating and 
    presenting static route edit-config data
    """
    def __init__(self, file_: dict, base_dir: str) -> None:
        super().__init__(file_, base_dir)
        self.template = self.j2_env.get_template("ip_route_config.xml")
        self.pretemplate_data = self.parse_data("ip_route")
        self.vrf_dict = self.create_vrf_dict()
        self.xml_config = self.render_model_xml()

    def print_config(self) -> str:
        """
        Return edit-config rpc for specific module
        """
        rendered_data = self.edit_template.render(ip_route=self.xml_config)
        return self.prettify_xml(rendered_data)

    def render_model_xml(self) -> str:
        """
        Takes it's own ip_route definition in yaml format in,
        uses ip_route_config.xml as a jinja2 template
        outputs a rendered xml netconf section
        """
        return self.template.render(vrf_dict=self.vrf_dict, ip_routes=self.pretemplate_data)

    def create_vrf_dict(self) -> dict:
        """
        Used for templating, parses through input ip_route yaml data
        returns a dictionary that can be later parsed by jinja2
        """
        vrf_routes = self.pretemplate_data.get("vrf")
        vrf_dict = defaultdict(list)
        if vrf_routes:
            for route in vrf_routes:
                vrf_dict[route["vrf"]].append(route)

        return vrf_dict
