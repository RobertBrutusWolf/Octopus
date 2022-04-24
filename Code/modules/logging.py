#Module that contains standard logging functions 

import traceback
from datetime import datetime
from pathlib import Path
from timeit import default_timer
from typing import *


from modules.global_class import GlobalClass

class Logging:
  
    def __init__(self):
        
        self.log_filename = GlobalClass.log_filename
        self.exception_filename = GlobalClass.exceptions_filename
          
 
    def write_log(self, message,level) -> bool:
       
        try:
            now = datetime.now()
            cdate = now.strftime("%d/%m/%Y %H:%M:%S")
            file_event_date = now.date().isoformat()

            log_dir = self.log_filename.parent
            filename = self.exception_filename if level == 'critical' else self.log_filename
            filename_with_date = log_dir / f'{file_event_date} {filename.name}'

            with filename_with_date.open('a') as f:
                log_message = f'{cdate}: {message}'
                f.write(log_message+'\n')
                print(log_message)
                
            return True
        except:
            print(f"Logging.write_log_to_file - Unexpected error:", traceback.format_exc())
            return False

    
