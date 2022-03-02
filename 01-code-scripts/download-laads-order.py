"""
-------------------------------------------------------------------------------
 Downloads a LAADS web order. The script will download files to
 the directory specified in the 'download_directory' variable. Any
 folders not existing in the specified path will be created during
 the download.

 Level-1 and Atmosphere Archive & Distribution System (LAADS) home:

   - https://ladsweb.modaps.eosdis.nasa.gov/about/purpose/

 Files can be searched for and data orders can be placed here:

   - https://ladsweb.modaps.eosdis.nasa.gov/search/

 User accounts (needed to obtain a token) can be created here:

   - https://urs.earthdata.nasa.gov/

 Download parameters (listed in the LAADS order completion email):

   -e robots=off : Bypass the robots.txt file, to allow access to all
                   files in the order

   -m            : Enable mirroring options (-r -N -l inf) for
                   recursive download, timestamping & unlimited depth

   -np           : Do not recurse into the parent location

   -R .html,.tmp : Reject (do not save) any .html or .tmp files (which
                   are extraneous to the order)

   -nH           : Do not create a subdirectory with the Host name
                   (ladsweb.modaps.eosdis.nasa.gov)

   --cut-dirs=3  : Do not create subdirectories for the first 3 levels
                   (archive/orders/{ORDER_ID})

   --header      : Adds the header with your appKey (which is encrypted
                   via SSL)

   -P            : Specify the directory prefix (may be relative or
                   absolute)

 This script requires that 'wget' is installed on the local machine.

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
# Set LAADS token (specific to user account) - choose option 1 or 2
# Option 1 - as environment variable)
token = os.environ.get("LAADS_TOKEN")
# Option 2 - as information in text file
with open(os.path.join("", "", "laads-token.txt", mode="r")) as file:
    token = file.readline()

# Set location for data downloaded
data_directory = os.path.join("02-raw-data", "nighttime-lights", "")

# Set order IDs (if more than one, max files per order is 2,000)
order_ids = [100000001, 100000002, 100000003]

# -------------------------DATA ACQUISITION---------------------------------- #
# Create list of download strings (one for each order ID)
download_strs = [
    (
        "wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=3 "
        f'"https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/{order_id}/" '
        f'--header "Authorization: Bearer {token}" -P {data_directory}'
    )
    for order_id in order_ids
]

# Download data
for download_str in download_strs:
    os.system(download_str)

# -------------------------SCRIPT COMPLETION--------------------------------- #
print("\n")
print("-" * (18 + len(os.path.basename(__file__))))
print(f"Completed script: {os.path.basename(__file__)}")
print("-" * (18 + len(os.path.basename(__file__))))
