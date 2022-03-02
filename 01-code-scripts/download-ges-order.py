"""
-------------------------------------------------------------------------------
 Downloads NASA Goddard Earth Sciences (GES) Data and Information
 Services Center (DISC) web order. This script downloads files listed
 in a text file from a web order.

 GES DISC home:

   - https://disc.gsfc.nasa.gov/

 Nitogen dioxide data:

   - https://disc.gsfc.nasa.gov/datasets/OMNO2d_003/summary

 Carbon monixide data:

   - https://disc.gsfc.nasa.gov/datasets/AIRS3STD_7.0/summary

 User accounts can be created here:

   - https://urs.earthdata.nasa.gov/

 This script requires that 'wget' is installed on the local machine.

 Run with admin to write to the '.crs_cookies' file.

 This script runs within the Conda environment specified in the
 'environment-py38.yml' file.
-------------------------------------------------------------------------------
 Author:  Cale Kochenour
 Contact: cxk525@psu.edu
 Updated: 3/2/2022
-------------------------------------------------------------------------------
"""
# -------------------------ENVIRONMENT SETUP--------------------------------- #
# Import packages
import os

# -------------------------USER-DEFINED VARIABLES---------------------------- #
# Set NASA Earthdata username
user_name = ""

# Set path to '.urs_cookies' file
cookies_file = os.path.join("", "", ".urs_cookies")

# Set path to file containing download links
data_links = os.path.join("", "", "ges-order.txt")

# Set location for data downloaded
data_directory = os.path.join("02-raw-data", "nitrogen-dioxide", "")
data_directory = os.path.join("02-raw-data", "carbon-monoxide", "")

# -------------------------DATA ACQUISITION---------------------------------- #
# Create download folder if not already existing
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

download_str = (
    f"wget --load-cookies {cookies_file} --save-cookies "
    f"{cookies_file} --auth-no-challenge=on --keep-session-cookies "
    f"--user={user_name} --ask-password --content-disposition -i "
    f"{data_directory} -P {data_directory}"
)

# Download data
os.system(download_str)

# -------------------------SCRIPT COMPLETION--------------------------------- #
print("\n")
print("-" * (18 + len(os.path.basename(__file__))))
print(f"Completed script: {os.path.basename(__file__)}")
print("-" * (18 + len(os.path.basename(__file__))))
