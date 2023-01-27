__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

import json


class JsonParser:
    """_summary_

    Attributes:

    Methods:

    """
    json_file = None
    data = None

    def __init__(self, json_file: str = None):
        self.json_file = json_file
        self.data = None

    def parse(self):
        """_summary_
        """
        with open(self.json_file) as f:
            self.data = json.load(f)

    def get_data(self):
        return self.data

    def get_parameter(self, parameter: str):
        """_summary_

        Args:
            parameter (str): _description_

        Returns:
            _type_: _description_
        """
        if self.data is None:
            self.parse()
        return self.data[parameter]
