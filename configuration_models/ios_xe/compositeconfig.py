"""
Author: James Duvall
Purpose: CompositeConfig abstract class definition
"""

from abc import abstractmethod, ABCMeta
import yaml
import logging


class CompositeConfig(metaclass=ABCMeta):
    """
    Abstract class for configs
    """

    def __init__(self, file_: str, base_dir: str) -> None:
        """
        Initialize common configuration for all child configs.
        """
        self.file_ = file_
        logging.warning(file_)
        with open(file_, "r", encoding="UTF-8") as config_raw:
            self.config = yaml.safe_load(config_raw)
        self.base_dir = base_dir

        #Jinja specific attributes
        self.j2_env = self.create_jinja_environment()
        self.edit_template = self.j2_env.get_template("edit_config.xml")

    @abstractmethod
    def print_config(self):
        """
        Return edit-config rpc for model
        """
        pass
    
    @abstractmethod
    def render_model_xml(self):
        """
        Render the configuration into the model's specific netconf config
        """
        pass
