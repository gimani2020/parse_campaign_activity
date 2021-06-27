# parse_campaign_activity
Python script to to parse active campaign_activity from raw_data.zip file  


### Prerequisites

linux machine
python 3.6 
raw_data_fiels.zip 

  

### Usage

1. sudo python 
2. (optional) sudo python  --zipfile 'raw_data_fiels.zip'  --dim 'Consumer_DimCampaign_Daily_FULL_20170707.txt.gz'
    
   
   
    <!-- USAGE EXAMPLES -->
## Usage assumption
   
   script run with sudo privileges (mking new dirs in /tmp folder)

   Zip files location is copied to script execution folder  or  task folder  ( '/tmp/harman_task/')
   
   argument(optional): Zip file name (default: 'raw_data_fiels.zip')
    
   argument(optional): 3.	Dimension file name (default:  'Consumer_DimCampaign_Daily_FULL_20170707.txt.gz') 
   
   Activity types are always the same 
   
    

