import json
import os
import sys
import logging

class StocksConfigurator(object):
    # Config id is the brokerage/site you are parsing from - e.g. Yahoo
    def __init__(self, config_id):
        self.config_id = config_id
        self._load_mapping_json()
    
    def _load_mapping_json(self):
        dir_path = os.path.abspath(os.path.dirname(__file__))
        full_file_path = os.path.join(dir_path, self.config_id + "_key_map.json")
        
        try:
            with open(full_file_path, "r") as raw_data:
                self.name_mapping = json.load(raw_data)
        except OSError:
            logging.error("Could not load config")
            self.name_mapping = {}
