"""
-------------------------------------------------------------------------------
 Module to work with mosaicking preprocessed VNP46A2 files.

 This module is used within the Conda environment specified in the
 'environment-py38.yml' file.
-------------------------------------------------------------------------------
 Author:  Cale Kochenour
 Contact: cxk525@psu.edu
 Updated: 3/2/2022
-------------------------------------------------------------------------------
"""
import datetime as dt


def julian_to_gregorian(date):
    """Converts Julian date (YYYJJJ) to Gregorian date (YYYYMMDD).

    Parameters
    ----------
    date : str
        Julian date (YYYYJJJ).

    Returns
    -------
    converted : str
        Gregorian date (YYYYMMDD).

    Example
    -------
    >>>
    >>>
    >>>
    >>>
    """
    # Convert date
    converted = dt.datetime.strptime(date, "%Y%j").strftime("%Y-%m-%d")

    return converted
