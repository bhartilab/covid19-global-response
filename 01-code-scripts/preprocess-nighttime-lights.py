"""
-------------------------------------------------------------------------------
 Preprocesses VIIRS VNP46A2 HDF5 files. This script takes raw data
 and completes the following preprocessing tasks on each file:

   - Extracts radiance and quality flag bands;
   - Masks radiance for fill values, clouds, and sea water;
   - Fills masked data with NaN values;
   - Creates a georeferencing transform;
   - Creates export metadata; and,
   - Exports preprocessed radiance to GeoTiff format.

 This scripts runs within the Conda environment specified in the
 'environment-py37.yml' file.
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
import viirs

# -------------------------USER-DEFINED VARIABLES---------------------------- #
# Set paths
input_folder = os.path.join("02-raw-data", "nighttime-lights", "")
output_folder = os.path.join("03-processed-data", "nighttime-lights", "")

# -------------------------DATA PREPROCESSING-------------------------------- #
# Preprocess each HDF5 file (extract bands, mask for fill values,
#  poor-quality, no retrieval, clouds, sea water, fill masked values
#  with NaN, export to GeoTiff)
hdf5_files = glob.glob(os.path.join(input_folder, "*.h5"))
processed_files = 0
total_files = len(hdf5_files)
for hdf5 in hdf5_files:
    viirs.preprocess_vnp46a2(hdf5_path=hdf5, output_folder=output_folder)
    processed_files += 1
    print(f"Preprocessed file: {processed_files} of {total_files}\n\n")

# -------------------------SCRIPT COMPLETION--------------------------------- #
print("\n")
print("-" * (18 + len(os.path.basename(__file__))))
print(f"Completed script: {os.path.basename(__file__)}")
print("-" * (18 + len(os.path.basename(__file__))))
