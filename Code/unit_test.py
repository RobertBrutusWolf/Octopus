import traceback
from datetime import datetime 
import os

from modules.global_class import GlobalClass
from modules.utilities import Utilities
from modules.logging import Logging
from modules.comms import Comms
from modules.process_data import ProcessData

utils = Utilities()
log = Logging()
comms = Comms()
processdata = ProcessData()


def write_log(message) -> bool:
       
        try:
            now = datetime.now()
            cdate = now.strftime("%d/%m/%Y %H:%M:%S")
            log_message = f'{cdate}: {message}'
            
            print(log_message)
            return True

        except:
            print(f"unit_test.write_log_to_file - Unexpected error:", traceback.format_exc())
            return False

def initialise_endpoints():
    
    result = False
    try:
        
        result = utils.read_config()
        write_log("Reading config = OK")   
        
       
        GlobalClass.base_endpoint = utils.get_config("application_settings", "base_endpoint", "string")
        GlobalClass.base_api_key = utils.get_config("application_settings", "base_api_key", "string")
        GlobalClass.outages_endpoint = GlobalClass.base_endpoint + utils.get_config("application_settings", "outages_endpoint", "string")
        GlobalClass.siteinfo_endpoint = GlobalClass.base_endpoint + utils.get_config("application_settings", "siteinfo_endpoint", "string")
        GlobalClass.siteoutages_endpoint = GlobalClass.base_endpoint + utils.get_config("application_settings", "siteoutages_endpoint", "string")
        GlobalClass.api_post_retries = utils.get_config("application_settings", "api_post_retries", "int")
        write_log("Setting Endpoints = OK")
        
    except Exception:
         log.write_log("app_run.initialise - Unexpected error:" + traceback.format_exc())
         

    return result

def main():
    result = None

    write_log("Starting Unit Tests")

    write_log("Testing Utilities Class")
    initialise_endpoints()

    filename = str(GlobalClass.requests_dir) + f'/testfile.dat'
    if (os.path.exists(filename)==True):
        os.remove(filename)

    utils.write_to_file(filename,"12345")
    if (os.path.exists(filename)==True):
        write_log("Utilities.write_to_file = OK")
        os.remove(filename)

    write_log("Testing Utilities Class")


    return result


try:
    if __name__ == "__main__":

        main()

except Exception:
     print(f"unit_test.main - Unexpected error:", traceback.format_exc())