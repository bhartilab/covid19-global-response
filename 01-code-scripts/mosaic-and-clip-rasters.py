"""
-------------------------------------------------------------------------------
 Mosaicks VNP46A2 tiles from the same date and clips the mosaic
 to a defined area of interest (shapefile).

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
from shapely.geometry import mapping
import rioxarray as rxr
from rioxarray.merge import merge_arrays
import geopandas as gpd
import mosaics as ms

# -------------------------USER-DEFINED VARIABLES---------------------------- #
# Set paths
input_folder = os.path.join("03-processed-data", "radiance", "", "")
output_folder = os.path.join("03-processed-data", "radiance", "", "")
aoi_path = os.path.join("02-raw-data", "aoi-boundaries", ".shp")

# -------------------------DATA PREPROCESSING-------------------------------- #
# Create output folder if not already existing
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Collect input files (individual tiles over all dates)
all_files = glob(os.path.join(input_folder, "*.tif"))

# Load AOI and project to raster CRS
aoi_wgs84 = gpd.read_file(aoi_path).to_crs(
    crs=rxr.open_rasterio(filename=all_files[0]).rio.crs
)

# Get unique dates (for mosaic images)
julian_dates = sorted(
    list(set([os.path.basename(file)[9:16] for file in all_files]))
)

# Mosaic, clip, and export (for each date)
for julian_date in julian_dates:
    # Get all files to mosaic (on same date)
    files_to_mosaic = [
        file
        for file in all_files
        if julian_date in os.path.basename(file)[9:16]
    ]
    print(
        f"Number of files to mosaic for "
        f"{ms.julian_to_gregorian(date=julian_date)}: "
        f"{len(files_to_mosaic)}"
    )
    # Read each same-day file into xarray
    xarray_list = [
        rxr.open_rasterio(filename=file) for file in files_to_mosaic
    ]
    # Spatially merge (mosaic) into single xarray
    xarray_mosaic = merge_arrays(dataarrays=xarray_list)
    # Clip mosaic to AOI
    xarray_clipped = xarray_mosaic.rio.clip(
        geometries=aoi_wgs84.geometry.apply(mapping),
        all_touched=True,
        drop=True,
        invert=False,
    )
    output_name = f"{ms.julian_to_gregorian(date=julian_date)}.tif"
    print(f"Output name: {output_name}")
    try:
        xarray_clipped.rio.to_raster(
            raster_path=os.path.join(output_folder, output_name)
        )
    except Exception as error:
        print(f"ERROR: {error}\n")
    else:
        print(f"Exported: {output_name}\n")

# -------------------------SCRIPT COMPLETION--------------------------------- #
print("\n")
print("-" * (18 + len(os.path.basename(__file__))))
print(f"Completed script: {os.path.basename(__file__)}")
print("-" * (18 + len(os.path.basename(__file__))))
