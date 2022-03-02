"""
-------------------------------------------------------------------------------
 Preprocesses OMI/Aura nitrogen dioxide netCDF4 files. This script
 takes raw data and completes the following preprocessing tasks:

   - Reads .nc file;
   - Isolates variables; and,
   - Exports each variable to GeoTiff.

 OMI/Aura data download:

   - https://disc.gsfc.nasa.gov/datasets/OMNO2d_003/summary

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
import glob
import rioxarray as rxr

# -------------------------USER-DEFINED VARIABLES---------------------------- #
# Set paths
input_folder = os.path.join("02-raw-data", "nitrogen-dioxide", "")
output_folder = os.path.join("03-processed-data", "nitrogen-dioxide", "")

# Set names for output folders (for each variable)
output_folders_dict = {
    "ColumnAmountNO2": "total-all-conditions",
    "ColumnAmountNO2CloudScreened": "total-cloud-screened",
    "ColumnAmountNO2Trop": "tropospheric-all-conditions",
    "ColumnAmountNO2TropCloudScreened": "tropospheric-cloud-screened",
    "Weight": "pixel-weights",
}

# -------------------------DATA PREPROCESSING-------------------------------- #
# Create output folder if not already existing
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Preprocess files
for nc_file in glob.glob(os.path.join(input_folder, "*.nc4")):
    # Extract date components
    year = os.path.basename(nc_file)[19:23]
    month = os.path.basename(nc_file)[24:26]
    day = os.path.basename(nc_file)[26:28]
    date = f"{year}-{month}-{day}"
    print(f"Processing date: {date}")
    # Assign CRS
    with rxr.open_rasterio(filename=nc_file, masked=True).squeeze() as file:
        no2 = file.rio.write_crs(input_crs="epsg:4326")
    # Isolate data variables, set nodata value, and export
    for variable_name in [
        "ColumnAmountNO2",
        "ColumnAmountNO2CloudScreened",
        "ColumnAmountNO2Trop",
        "ColumnAmountNO2TropCloudScreened",
        "Weight",
    ]:
        variable_data = no2[variable_name]
        export_path = os.path.join(
            output_folder,
            output_folders_dict.get(variable_name),
            f"{date}.tif",
        )
        if not os.path.exists(
            os.path.join(output_folder, output_folders_dict.get(variable_name))
        ):
            os.mkdir(
                os.path.join(
                    output_folder, output_folders_dict.get(variable_name)
                )
            )
        variable_data.rio.to_raster(raster_path=export_path)
    print(f"Processed date: {date}\n")

# -------------------------SCRIPT COMPLETION--------------------------------- #
print("\n")
print("-" * (18 + len(os.path.basename(__file__))))
print(f"Completed script: {os.path.basename(__file__)}")
print("-" * (18 + len(os.path.basename(__file__))))
