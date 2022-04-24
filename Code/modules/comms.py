from requests.auth import HTTPBasicAuth
import requests
import traceback
import json
import time


from modules.global_class import GlobalClass
from modules.logging import Logging
from modules.utilities import Utilities


class Comms:

    log = Logging()
    utils = Utilities()

    def get_outages(self):
        result = None
        try:
            #build headers
            headers = {'Accept': 'application/json','x-api-key' : GlobalClass.base_api_key}
               
            #perform get and convert data
            req = requests.get(GlobalClass.outages_endpoint, headers=headers)
            result = req.json()
          

        except Exception:
            self.log.write_log(f"utilities.get_outages : Unexpected error" + traceback.format_exc(), level='critical')

        return result

    def get_site_info(self,siteinfo):
        result = None
        try:

            #build header and siteurl
            headers = {'Accept': 'application/json','x-api-key' : GlobalClass.base_api_key}
            siteurl = GlobalClass.siteinfo_endpoint + "/" + siteinfo

            #perform get and convert data
            req = requests.get(siteurl, headers=headers)
            result = req.json()
           

        except Exception:
            self.log.write_log(f"utilities.get_site_info : Unexpected error" + traceback.format_exc(), level='critical')

        return result

    def post_filteredoutages(self, outages_df,site_outages_url):
        result = None
        try:
            #build headers
            headers = {'x-api-key' : GlobalClass.base_api_key}
            
            #build pretty json data for logs
            json_data = outages_df.to_json(orient="records", indent=2)
            
            #writes out the post to the local file for auditing
            requests_filename = str(GlobalClass.requests_dir) + f'/sent_' + GlobalClass.app_uuid + ".json"
            self.utils.write_to_file(requests_filename,json_data)

            #build non pretty json data for post
            json_data = outages_df.to_json(orient="records")
     
            #set post counter and inital status code
            post_counter = 1
            status_code = 500

            while((status_code!=200 and status_code!=201) and post_counter<=GlobalClass.api_post_retries):
                self.log.write_log(f'Send Attempt {post_counter}', level='info')
                try:

                    #perform post and retrieve status code
                    req = requests.post(site_outages_url, headers=headers, data=json_data)
                    status_code = req.status_code
                    content = req.json()

                except Exception:
                    post_counter = GlobalClass.api_post_retries+1
                    self.log.write_log(f"utilities.post_filteredoutages : Unexpected error" + traceback.format_exc(), level='critical')
                    
                #if error then write the logs and increase counter. Pause 1 seconds just incase of api issues
                if (status_code!=200 and status_code!=201):
                    self.log.write_log(f'Failed to send status code - {status_code}', level='info')
                    self.log.write_log(f'Failed response - {content}', level='info')
                    post_counter = post_counter + 1
                    time.sleep(1)
                                              
        except Exception:
            self.log.write_log(f"utilities.post_filteredoutages : Unexpected error" + traceback.format_exc(), level='critical')

        return result