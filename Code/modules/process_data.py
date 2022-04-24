import os
import uuid
import pandas as pd
import pandasql as psql
import uuid
import datetime

import traceback
import json

from modules.logging import Logging
from modules.global_class import GlobalClass
from modules.utilities import Utilities

class ProcessData:

    log = Logging()
    utils = Utilities()

    def filter_data(self,outages_json,site_info_json,outage_max_date):
        result = None
        try:
            #extract device list from json
            devices = site_info_json["devices"]

            #convert outages to a dataframe
            outages = pd.DataFrame(outages_json)

            #convert siteinfo to dataframe
            siteinfo = pd.DataFrame(devices)
            

            #3. Filters out any outages that began before `2022-01-01T00:00:00.000Z` or don't have an ID that is in the list of
            #devices in the site information
            #4. For the remaining outages, it should attach the display name of the device in the site information to each appropriate outage

            #transform the data
            strsql = f"select outages.id,siteinfo.name,outages.begin,outages.end from outages inner join siteinfo on outages.id=siteinfo.id where outages.begin>='{outage_max_date}'"
            result = psql.sqldf(strsql, locals())

            

        except Exception:
                self.log.write_log(f"ProcessData.json_to_dataframe : Unexpected error" + traceback.format_exc(), level='critical')

        return result

