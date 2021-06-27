# parse_campaign_activity
Python script to to parse active campaign_activity from raw_data.zip file  


### Prerequisites

linux machine

python 3.6

raw_data_fiels.zip 

  

### Usage

1. sudo python campaign_activity.py
2. (optional) sudo python campaign_activity.py  --zipfile 'raw_data_fiels.zip'  --dim 'Consumer_DimCampaign_Daily_FULL_20170707.txt.gz'
    
   
   
    <!-- USAGE EXAMPLES -->
## Usage assumption
   
   Script run with sudo privileges (making new dirs in /tmp folder)

   Zip files location is copied to script execution folder  or  task folder  ( '/tmp/harman_task/')
   
   Argument(optional): Zip file name (default: 'raw_data_fiels.zip')
    
   Argument(optional): 3.	Dimension file name (default:  'Consumer_DimCampaign_Daily_FULL_20170707.txt.gz') 
   
   Activity types are always the same 
   
   Remove all debug prints (wait till script finish)   
   
    

