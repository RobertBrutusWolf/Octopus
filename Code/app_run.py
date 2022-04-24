
import os
import sys
import json
import logging as comms_logging

import logging.handlers as handlers
import socket
import time
import uuid
import warnings
import threading
from datetime import datetime,timezone
from pathlib import Path
from typing import *
import importlib
import glob
import traceback
import pandas



from modules.global_class import GlobalClass
from modules.utilities import Utilities
from modules.logging import Logging
from modules.comms import Comms
from modules.process_data import ProcessData

warnings.simplefilter(action='ignore')

FILENAME = Path(__file__).name

# create new components instances
log = Logging()
utils = Utilities()
comms = Comms()
processdata = ProcessData()

def createDefaultDirs():
 # creating non-default project directories
    try:
        
        dirs_to_create = [GlobalClass.runtime_data_dir, GlobalClass.logs_local_ip_dir, GlobalClass.requests_dir]
        for path in dirs_to_create:
            path.mkdir(exist_ok=True, parents=True)

    except Exception:
        print("app_run.createDefaultDirs - Unexpected error:" + traceback.format_exc())

def initialise_endpoints():
    
    result = False
    try:
        #read the config file in to the array within the utils class
        result = utils.read_config()
       
        #populates the static singleton properties so they can be used within the code. 

        GlobalClass.base_endpoint = utils.get_config("application_settings", "base_endpoint", "string")
        GlobalClass.base_api_key = utils.get_config("application_settings", "base_api_key", "string")
        GlobalClass.outages_endpoint = GlobalClass.base_endpoint + utils.get_config("application_settings", "outages_endpoint", "string")
        GlobalClass.siteinfo_endpoint = GlobalClass.base_endpoint + utils.get_config("application_settings", "siteinfo_endpoint", "string")
        GlobalClass.siteoutages_endpoint = GlobalClass.base_endpoint + utils.get_config("application_settings", "siteoutages_endpoint", "string")
        GlobalClass.api_post_retries = utils.get_config("application_settings", "api_post_retries", "int")
  
        
    except Exception:
         log.write_log("app_run.initialise - Unexpected error:" + traceback.format_exc(), level='critical')
         

    return result

def main():
   
    try:
            log.write_log(f'Starting App', level='info')
                   
            #Retrieves all outages from the `GET /outages` endpoint
            log.write_log(f'Retrieve all outages from ' + GlobalClass.outages_endpoint, level='info')
            outages_json_data = comms.get_outages()
            outage_count =len(outages_json_data)
            log.write_log(f'Recieved {outage_count} outages', level='info')

            #Retrieves information from the `GET /site-info/{siteId}` endpoint for the site with the ID `norwich-pear-tree`
            site = utils.get_config("application_settings", "site_info", "string")
            log.write_log(f'Retrieve site info for {site}', level='info')
            site_info_json_data = comms.get_site_info(site)
            device_count = len(site_info_json_data["devices"])
            log.write_log(f'Recieved {device_count} devices for {site}', level='info')
            

            #Filters out any outages that began before `2022-01-01T00:00:00.000Z` or don't have an ID that is in the list of devices in the site information
            outage_max_date = datetime.fromisoformat(utils.get_config("application_settings", "outage_max_date", "string")[:-1]).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            log.write_log(f'Filtering and Transform Data by outage date before {outage_max_date}' , level='info')
            outages_df = processdata.filter_data(outages_json_data,site_info_json_data,outage_max_date)
            filtered_count = len(outages_df)
            log.write_log(f'Filtered results to {filtered_count} outage(s)', level='info')

            #Sends this list of outages to `POST /site-outages/{siteId}` for the site with the ID `norwich-pear-tree`
            site_outages_url = GlobalClass.siteoutages_endpoint + f'/{site}'

            log.write_log(f'Send Data to ' + site_outages_url, level='info')
            comms.post_filteredoutages(outages_df,site_outages_url)

            log.write_log(f'Stopped App', level='info')

    except Exception:
        log.write_log("app_run.main - Unexpected error:" + traceback.format_exc(), level='critical')

         
try:
    if __name__ == "__main__":
      
        createDefaultDirs()

        log.write_log(GlobalClass.app_name + '  version=' + GlobalClass.app_version, level='info')
        if (initialise_endpoints()==True):
            main()
        else:
            print(f"app_run - Unable to start due to " + GlobalClass.app_config_filename + " error:", traceback.format_exc())
except Exception:
     print(f"app_run.main - Unexpected error:", traceback.format_exc())