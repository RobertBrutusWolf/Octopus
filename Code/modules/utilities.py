#Module containing utility functions

import os
import json

from typing import *
from uuid import UUID
from pathlib import Path
import numpy as np
import traceback

from modules.global_class import GlobalClass
from modules.logging import Logging

class Utilities:
    log = Logging()

    def write_to_file(self, filename,data):
       
        try:
            with open(filename, 'w') as writefile:
                writefile.write(data)
                writefile.close()
                
            return True
        except:
            print(f"Logging.write_to_file - Unexpected error:", traceback.format_exc())
            return False

    def read_config(self):
        result = False
        self.log.write_log(f"Reading config file '{GlobalClass.app_config_filename}'", level='info')
        
        try:
            
            if os.path.exists(GlobalClass.app_config_filename):
                with GlobalClass.app_config_filename.open() as f:
                    GlobalClass.config_data = json.load(f)
                result = True

        except OSError as err:
            self.log.write_log("utilities.read_config : OS error: " + traceback.format_exc(), level='critical')

        return result

    def get_config(self, header, key, var_type):

        result = ''
        try:

            if os.getenv(key) is not None:
                str_result = os.getenv(key)
                self.log.write_log("get_template_config : template_config setting " + key + " set by env var to '" + str_result + "'", level='info')
            else:
                str_result = GlobalClass.config_data[header][0][key]
                
            test_str_result = str(str_result).replace('[', '').replace(']', '')

            if var_type == 'int':
                result = np.fromstring(test_str_result, dtype=int, sep=',')
            if var_type == 'float':
                result = np.fromstring(test_str_result, dtype=float, sep=',')
            if var_type == 'bool':
                result = bool(str_result)
            if var_type == 'string':
                result = str_result

        except Exception:
            self.log.write_log(f"utilities.get_config : Unexpected error" + traceback.format_exc(), level='critical')

        return result

    
