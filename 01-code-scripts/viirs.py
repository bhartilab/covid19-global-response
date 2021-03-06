"""
-------------------------------------------------------------------------------
 Module to work with NASA VIIRS nighttime lights data.

 Designed for "VNP46A2 - VIIRS/NPP Gap-Filled Lunar BRDF-Adjusted
 Nighttime Lights Daily L3 Global 500m Linear Lat Lon Grid" data.

 VNP46A2 data home:

   - https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A2/

 VNP46A2 data download:

   - https://ladsweb.modaps.eosdis.nasa.gov/search/order/1/VNP46A2--5000

 This module is used within the Conda environment specified in the
 'environment-py37.yml' file.
-------------------------------------------------------------------------------
 Author:  Cale Kochenour
 Contact: cxk525@psu.edu
 Updated: 3/2/2022
-------------------------------------------------------------------------------
"""
import os
import re
import numpy as np
import numpy.ma as ma
import rasterio as rio
from rasterio.transform import from_origin


def create_metadata(
    array, transform, driver="GTiff", nodata=0, count=1, crs="epsg:4326"
):
    """Creates export metadata, for use with
    exporting an array to raster format.

    Parameters
    ----------
    array : numpy array
        Array containing data for export.

    transform : rasterio.transform affine object
        Affine transformation for the georeferenced array.

    driver : str
        File type/format for export. Defaults to GeoTiff ('GTiff').

    nodata : int or float
        Value in the array indicating no data. Defaults to 0.

    count : int
        Number of bands in the array for export. Defaults to 1.

    crs : str
        Coordinate reference system for the georeferenced
        array. Defaults to EPSG 4326 ('epsg:4326').

    Returns
    -------
    metadata : dict
        Dictionary containing the export metadata.

    Example
    -------
        >>> # Imports
        >>> import numpy as np
        >>> from rasterio.transform import from_origin
        >>> # Create array
        >>> arr = np.array([[1,2],[3,4]])
        >>> transform = from_origin(-73.0, 43.0, 0.5, 0.5)
        >>> meta = create_metadata(arr, transform)
        # Display metadata
        >>> meta
        {'driver': 'GTiff',
         'dtype': dtype('int32'),
         'nodata': 0,
         'width': 2,
         'height': 2,
         'count': 1,
         'crs': 'epsg:4326',
         'transform': Affine(0.5, 0.0, -73.0,
                0.0, -0.5, 43.0)}
    """
    # Define metadata
    metadata = {
        "driver": driver,
        "dtype": array.dtype,
        "nodata": nodata,
        "width": array.shape[1],
        "height": array.shape[0],
        "count": count,
        "crs": crs,
        "transform": transform,
    }

    return metadata


def create_transform_vnp46a2(hdf5):
    """Creates a geographic transform for a VNP46A2 HDF5 file,
    based on longitude bounds, latitude bounds, and cell size.

    Parameters
    ----------
    hdf5 : str
        Path to an existsing VNP46A1 HDF5 file.

    Returns
    -------
    transform : affine.Affine object
        Affine transformation for the georeferenced array.

    Example
    -------
        >>>
        >>>
        >>>
        >>>
    """
    # Extract bounding box from top-level dataset
    with rio.open(hdf5) as dataset:
        longitude_min = int(dataset.tags()["WestBoundingCoord"])
        longitude_max = int(dataset.tags()["EastBoundingCoord"])
        latitude_min = int(dataset.tags()["SouthBoundingCoord"])
        latitude_max = int(dataset.tags()["NorthBoundingCoord"])

        # Extract number of row and columns from first
        #  Science Data Set (subdataset/band)
        with rio.open(dataset.subdatasets[0]) as band:
            num_rows, num_columns = (
                band.meta.get("height"),
                band.meta.get("width"),
            )

    # Define transform (top-left corner, cell size)
    transform = from_origin(
        longitude_min,
        latitude_max,
        (longitude_max - longitude_min) / num_columns,
        (latitude_max - latitude_min) / num_rows,
    )

    return transform


def export_array(array, output_path, metadata):
    """Exports a numpy array to a GeoTiff.

    Parameters
    ----------
    array : numpy array
        Numpy array to be exported to GeoTiff.

    output_path : str
        Path to the output file (includeing filename).

    metadata : dict
        Dictionary containing the metadata required
        for export.

    Returns
    -------
    output_message : str
        Message indicating success or failure of export.

    Example
    -------
        >>> # Define export output paths
        >>> radiance_mean_outpath = os.path.join(
        ...     output_directory,
        ...     "radiance-mean.tif")
        # Define export transform
        >>> transform = from_origin(
        ...     lon_min,
        ...     lat_max,
        ...     coord_spacing,
        ...     coord_spacing)
        >>> # Define export metadata
        >>> export_metadata = {
        ...     "driver": "GTiff",
        ...     "dtype": radiance_mean.dtype,
        ...     "nodata": 0,
        ...     "width": radiance_mean.shape[1],
        ...     "height": radiance_mean.shape[0],
        ...     "count": 1,
        ...     "crs": 'epsg:4326',
        ...     "transform": transform
        ... }
        >>> # Export mean radiance
        >>> export_array(
        >>>     array=radiance_mean,
        >>>     output_path=radiance_mean_outpath,
        >>>     metadata=export_metadata)
        Exported: radiance-mean.tif
    """
    # Write numpy array to GeoTiff
    try:
        with rio.open(output_path, "w", **metadata) as dst:
            dst.write(array, 1)
    except Exception as error:
        output_message = print(f"ERROR: {error}")
    else:
        output_message = print(f"Exported: {os.path.split(output_path)[-1]}")

    return output_message


def extract_band_vnp46a2(hdf5_path, band_name):
    """Extracts the specified band (Science Data Set) from a NASA VNP46A2
    HDF5 file.

    Available Science Data Sets include:

    DNB_BRDF-Corrected_NTL
    DNB_Lunar_Irradiance
    Gap_Filled_DNB_BRDF-Corrected_NTL
    Latest_High_Quality_Retrieval
    Mandatory_Quality_Flag
    QF_Cloud_Mask
    Snow_Flag

    Parameters
    ----------
    hdf5_path : str
        Path to the VNP46A2 HDF5 (.h5) file.

    band_name : str
        Name of the band (Science Data Set) to be extracted. Must be an exact
        match to an available Science Data Set.

    Returns
    -------
    band : numpy array
        Array containing the data for the specified band (Science Data Set).

    Example
    -------
        >>> qf_cloud_mask = extract_band_vnp46a2(
        ...     hdf5='VNP46A2.A2016153.h30v05.001.2020267141459.h5',
        ...     band='QF_Cloud_Mask'
        ... )
        >>> type(qf_cloud_mask)
        numpy.ndarray
    """
    # Raise error for invalid band name
    band_names = [
        "DNB_BRDF-Corrected_NTL",
        "DNB_Lunar_Irradiance",
        "Gap_Filled_DNB_BRDF-Corrected_NTL",
        "Latest_High_Quality_Retrieval",
        "Mandatory_Quality_Flag",
        "QF_Cloud_Mask",
        "Snow_Flag",
    ]
    if band_name not in band_names:
        raise ValueError(
            f"Invalid band name. Must be one of the following: {band_names}"
        )

    # Open top-level dataset, loop through Science Data Sets (subdatasets),
    #  and extract specified band
    with rio.open(hdf5_path) as dataset:
        for science_data_set in dataset.subdatasets:
            if re.search(f"{band_name}$", science_data_set):
                with rio.open(science_data_set) as src:
                    band = src.read(1)

    return band


def extract_qa_bits(qa_band, start_bit, end_bit):
    """Extracts the QA bitmask values for a specified bitmask (starting
     and ending bit).

    Parameters
    ----------
    qa_band : numpy array
        Array containing the raw QA values (base-2) for all bitmasks.

    start_bit : int
        First bit in the bitmask.

    end_bit : int
        Last bit in the bitmask.

    Returns
    -------
    qa_values : numpy array
        Array containing the extracted QA values (base-10) for the
        bitmask.

    Example
    -------
        >>>
        >>>
        >>>
        >>>
    """
    # Initialize QA bit string/pattern to check QA band against
    qa_bits = 0

    # Add each specified QA bit flag value/string/pattern
    #  to the QA bits to check/extract
    for bit in range(start_bit, end_bit + 1):
        qa_bits += bit ** 2

    # Check QA band against specified QA bits to see what
    #  QA flag values are set
    qa_flags_set = qa_band & qa_bits

    # Get base-10 value that matches bitmask documentation
    #  (0-1 for single bit, 0-3 for 2 bits, or 0-2^N for N bits)
    qa_values = qa_flags_set >> start_bit

    return qa_values


def preprocess_vnp46a2(hdf5_path, output_folder):
    """Preprocessed a NASA VNP46A2 HDF5 (.h5 file)

    Preprocessing steps include masking data for fill values, clouds, and
    sensor problems, filling masked values, and exporting data to a GeoTiff.

    Parameters
    ----------
    hdf5_path : str
        Path to the VNP46A2 HDF5 (.h5) file to be preprocessed.

    output_folder : str
        Path to the folder where the preprocessed file will be exported to.

    Returns
    -------
    message : str
        Indication of preprocessing completion status (success or failure).

    Example
    -------
        >>>
        >>>
        >>>
        >>>
    """
    # Preprocess VNP46A2 HDF5 file
    print(f"Started preprocessing: {os.path.basename(hdf5_path)}")
    try:
        print("Extracting bands...")
        # Extract DNB BRDF-Corrected radiance
        dnb_brdf_corrected_ntl = extract_band_vnp46a2(
            hdf5_path=hdf5_path, band_name="DNB_BRDF-Corrected_NTL"
        )

        # Extract Mandatory Quality Flag, QF Cloud Mask, and Snow Flag bands
        mandatory_quality_flag = extract_band_vnp46a2(
            hdf5_path=hdf5_path, band_name="Mandatory_Quality_Flag"
        )
        qf_cloud_mask = extract_band_vnp46a2(
            hdf5_path=hdf5_path, band_name="QF_Cloud_Mask"
        )

        print("Applying scale factor...")
        # Apply scale factor to radiance values
        dnb_brdf_corrected_ntl_scaled = (
            dnb_brdf_corrected_ntl.astype("float") * 0.1
        )

        print("Masking for fill values...")
        # Mask radiance for fill value (dnb_brdf_corrected_ntl == 65535)
        masked_for_fill_value = ma.masked_where(
            dnb_brdf_corrected_ntl_scaled == 6553.5,
            dnb_brdf_corrected_ntl_scaled,
            copy=True,
        )

        print("Masking for poor quality and no retrieval...")
        # Mask radiance for 'poor quality' (mandatory_quality_flag == 2)
        masked_for_poor_quality = ma.masked_where(
            mandatory_quality_flag == 2, masked_for_fill_value, copy=True
        )

        # Mask radiance for 'no retrieval' (mandatory_quality_flag == 255)
        masked_for_no_retrieval = ma.masked_where(
            mandatory_quality_flag == 255, masked_for_poor_quality, copy=True
        )

        print("Masking for clouds...")
        # Extract QF_Cloud_Mask bits 6-7 (Cloud Detection Results &
        #  Confidence Indicator)
        cloud_detection_bitmask = extract_qa_bits(
            qa_band=qf_cloud_mask, start_bit=6, end_bit=7
        )

        # Mask radiance for 'probably cloudy' (cloud_detection_bitmask == 2)
        masked_for_probably_cloudy = ma.masked_where(
            cloud_detection_bitmask == 2, masked_for_no_retrieval, copy=True
        )

        # Mask radiance for 'confident cloudy' (cloud_detection_bitmask == 3)
        masked_for_confident_cloudy = ma.masked_where(
            cloud_detection_bitmask == 3, masked_for_probably_cloudy, copy=True
        )

        print("Masking for sea water...")
        # Extract QF_Cloud_Mask bits 1-3 (Land/Water Background)
        land_water_bitmask = extract_qa_bits(
            qa_band=qf_cloud_mask, start_bit=1, end_bit=3
        )

        # Mask radiance for sea water (land_water_bitmask == 3)
        masked_for_sea_water = ma.masked_where(
            land_water_bitmask == 3, masked_for_confident_cloudy, copy=True
        )

        print("Filling masked values...")
        # Set fill value to np.nan and fill masked values
        ma.set_fill_value(masked_for_sea_water, np.nan)
        filled_data = masked_for_sea_water.filled()

        print("Creating metadata...")
        # Create metadata (for export)
        metadata = create_metadata(
            array=filled_data,
            transform=create_transform_vnp46a2(hdf5_path),
            driver="GTiff",
            nodata=np.nan,
            count=1,
            crs="epsg:4326",
        )

        print("Exporting to GeoTiff...")
        # Export masked array to GeoTiff (no data set to np.nan in export)
        export_name = (
            f"{os.path.basename(hdf5_path)[:-3].lower().replace('.', '-')}.tif"
        )
        export_array(
            array=filled_data,
            output_path=os.path.join(output_folder, export_name),
            metadata=metadata,
        )
    except Exception as error:
        message = print(f"Preprocessing failed: {error}\n")
    else:
        message = print(
            f"Completed preprocessing: {os.path.basename(hdf5_path)}\n"
        )

    return message
