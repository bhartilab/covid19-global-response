"""
-------------------------------------------------------------------------------
 Preprocesses Aqua/AIRS carbon monoxide netCDF4 files. This script
 takes raw data and completes the following preprocessing tasks:

   - Reads .nc file; and,
   - Exports to GeoTiff.

 Aqua/AIRS data download:

   - https://disc.gsfc.nasa.gov/datasets/AIRS3STD_7.0/summary

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
from glob import glob
import rioxarray as rxr

# -------------------------USER-DEFINED VARIABLES---------------------------- #
# Set paths
input_folder = os.path.join("02-raw-data", "carbon-monoxide", "", "")
output_folder = os.path.join("03-processed-data", "carbon-monoxide", "", "")

# -------------------------DATA PREPROCESSING-------------------------------- #
# Create output folder if not already existing
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Preprocess files
for file in glob(os.path.join(input_folder, "*.nc4")):
    # Extract date
    basename = os.path.basename(file)
    date = f"{basename[5:9]}-{basename[10:12]}-{basename[13:15]}"
    # Read data and assign CRS
    print(f"Processing date: {date}")
    data = (
        rxr.open_rasterio(filename=file)
        .squeeze()
        .rio.write_crs(input_crs="epsg:4326", inplace=True)
    )
    # Export to GeoTiff
    data.rio.to_raster(os.path.join(output_folder, f"{date}.tif"))
    print(f"Processed date: {date}\n")

# -------------------------SCRIPT COMPLETION--------------------------------- #
print("\n")
print("-" * (18 + len(os.path.basename(__file__))))
print(f"Completed script: {os.path.basename(__file__)}")
print("-" * (18 + len(os.path.basename(__file__))))
