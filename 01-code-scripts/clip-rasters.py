"""
-------------------------------------------------------------------------------
 Clips GeoTiff files to a defined area of interest (shapefile). Used
 to clip nitrogen dioxide and carbon monoxide data.

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
import geopandas as gpd

# -------------------------USER-DEFINED VARIABLES---------------------------- #
# Set paths
input_folder = os.path.join("03-processed-data", "nitrogen-dioxide", "")
output_folder = os.path.join("03-processed-data", "nitrogen-dioxide", "")
input_folder = os.path.join("03-processed-data", "carbon-monoxide", "")
output_folder = os.path.join("03-processed-data", "carbon-monoxide", "")
aoi_path = os.path.join("02-raw-data", "aoi-boundaries", ".shp")

# -------------------------DATA PREPROCESSING-------------------------------- #
# Get files for clipping
all_files = glob(os.path.join(input_folder, "*tif"))

# Load AOI and project to raster CRS
aoi = gpd.read_file(aoi_path).to_crs(
    crs=rxr.open_rasterio(filename=all_files[0]).rio.crs
)

# Clip all files to AOI and export to GeoTiff
for file in all_files:
    # Read data
    data = (
        rxr.open_rasterio(filename=file)
        .squeeze()
        .rio.write_crs(input_crs="epsg:4326", inplace=True)
    )
    # Clip data
    data_clipped = data.rio.clip(
        geometries=aoi.geometry.apply(mapping),
        all_touched=True,
        drop=True,
        invert=False,
    )
    # Export to GeoTiff
    data_clipped.rio.to_raster(
        os.path.join(output_folder, os.path.basename(file),)
    )
    print(f"Clipping: {os.path.basename(file).replace('.tif', '')}")

# -------------------------SCRIPT COMPLETION--------------------------------- #
print("\n")
print("-" * (18 + len(os.path.basename(__file__))))
print(f"Completed script: {os.path.basename(__file__)}")
print("-" * (18 + len(os.path.basename(__file__))))
