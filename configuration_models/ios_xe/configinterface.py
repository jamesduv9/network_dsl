"""
Author: James Duvall
module: configinterface.py
purpose: Creates the subordinate configs
notes: Not super excited with how this is currently implemented, will consider rework
"""


from .compositeconfig import CompositeConfig
from .staticroutes import StaticRoutes
from .routerbgp import RouterBgp
from .prefixlist import PrefixList
from .utilityconfig import UtilityConfig
from .phyinterface import PhyInterface
from .routemap import RouteMap
from .nccwrapper import NccWrapper


class ConfigInterface(CompositeConfig, UtilityConfig, NccWrapper):
    """
    Initiates the creation of child configs
    Renders final xml edit-config rpc data
    """

    def __init__(self, file_: str, base_dir: str) -> None:
        super().__init__(file_=file_, base_dir=base_dir)
        configuration_map = {
            "router_bgp": self.create_routerbgp,
            "ip_route": self.create_staticroutes,
            "prefix_list": self.create_prefixlist,
            "route_map": self.create_routemap,
            "interface": self.create_interfaces,
        }
        self.config_objects = {}

        for k, _ in configuration_map.items():
            if self.config.get("device").get(k):
                configuration_map[k]()

        self.final_rpc = self.print_config()

    def create_interfaces(self) -> None:
        """
        Creates interface classes and adds it to the config_object dict
        """
        if self.config.get("device").get("interface").get("physical_interfaces"):
            self.config_objects["physical_interfaces"] = PhyInterface(
                file_=self.file_, base_dir=self.base_dir
            )

    def create_routemap(self) -> None:
        """
        Creates a RouteMap object and adds it to the config_objects dict
        """
        self.config_objects["route_map"] = RouteMap(
            file_=self.file_, base_dir=self.base_dir
        )

    def create_routerbgp(self) -> None:
        """
        Creates a RouterBgp object and adds it to the config_objects dict
        """
        self.config_objects["bgp"] = RouterBgp(file_=self.file_, base_dir=self.base_dir)

    def create_staticroutes(self) -> None:
        """
        Creates a StaticRoutes object and adds it to the config_objects dict
        """
        self.config_objects["ip_route"] = StaticRoutes(
            file_=self.file_, base_dir=self.base_dir
        )

    def create_prefixlist(self) -> None:
        """
        Creates a PrefixList object and adds it to the config_object dict
        """
        self.config_objects["prefix_list"] = PrefixList(
            file_=self.file_, base_dir=self.base_dir
        )

    def print_config(self) -> str:
        """
        Renders final xml edit-config rpc from all config_object values
        """
        rendered_output = self.edit_template.render(
            **{
                xml_key: xml_value.xml_config
                for xml_key, xml_value in self.config_objects.items()
            }
        )
        return self.prettify_xml(rendered_output)

    def render_model_xml(self):
        return self.print_config()
