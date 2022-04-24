#Module containing singelton class that acts as global namespace for paths, template configurations etc

import os
import socket
import traceback
import uuid
import queue
from datetime import datetime
from pathlib import Path
from typing import *
import threading


today = datetime.now().date().isoformat()
today_fmt = today.replace("-", "")

class GlobalClass:
    #note : The global class is for declaration of static properties and should not inherit any other classes or code
    #adding other classes or code causes circular references!

    #THIS CLASS NEEDS TO BE IMPORTED INTO EVERY CODE FILE UNDER THE TEMPLATE!


    app_name = "MockAPI"
    app_version = "R1 v1.0.0"
    app_uuid = str(uuid.uuid1())
    local_ip = socket.gethostbyname(socket.gethostname()).replace('.', '')
  
    ROOT = Path(__file__).parent.parent
    project_name = ROOT.name

    src_dir = ROOT / 'src'
    
    runtime_data_dir = ROOT / "runtime_data"

    sample_data_dir = runtime_data_dir / "sample_data"
    requests_dir = sample_data_dir / 'requests'
   
    app_config_filename = runtime_data_dir / 'config' / "app_config.json"
   
    logs_dir = runtime_data_dir / 'logs'
    logs_local_ip_dir = logs_dir / local_ip
    log_filename = logs_local_ip_dir / "log_file.txt"
    exceptions_filename = logs_local_ip_dir / "exceptions.txt"

    config_data = {}

    base_endpoint = ""
    base_api_key = ""
    outages_endpoint = ""
    siteinfo_endpoint = ""
    siteoutages_endpoint = ""
    api_post_retries = 0
  