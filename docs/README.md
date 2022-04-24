# KrakenFlex Test

#Author : Robert Wolf
#Date Created : 22/04/2022
#Python Version : 3.7



#Introduction
This app was built to meet the design specifications of the KrakenFLex test. The code has been structured using OOP principles, easy to read, code re-use and also spread across multiple classes to compartmentalise functionality 

I have provided a production ready codebase with full exception handling and logging functionality.

##Components
The list of components for the app and the pip commands used are located in /docs/component_install.txt

##Docker image
I have supplied a dockerfile and requirement.txt but due to time been unable to test it fully. 


##Configuration
All configuration for the application is stored in the runtime_data/config/app_config.json file. API endpoints and filter criterias can be changed here


##Logging
The app logs nearly all errors and info logs to the runtime/logs folder. Note - Specifying critical for log level on the log.write_log creates and appends to an exceptions file. 



##code files

app_run.py - main code and logic workflow
modules/comms.py - class for accessing endpoints
modules/global_class.py -  singleton/static class that supplies config across the app
modules/logging.py - class to provide logging functions to the code base
modules/process_data.py - class that transforms and filters data from the endpoints
modules/utilities.py - class that provides common functions to the codebase


#runtime


#possible refinements
1. clean up of log files and incoming json files. 
2. Write all logs out to AWS CloudWatch or GCP Logging. 
3. NOtifications on failures, errors on logs

