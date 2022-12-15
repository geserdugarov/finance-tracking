import os
import logging
import pandas as pd


logger = logging.getLogger(__name__)
logger.info("Loaded %s module." % __name__)


def find_file(data_folder: str, file_key: str) -> str:
    """
    Search for the file with file_key in filename

    Parameters
    ----------
    data_folder:  path to the folder for searching
    file_key:     the last file is used, which contain file_key in filename

    Return
    ----------
    Path to the last file with 'file_key' in filename.
    """
    for file in reversed(os.listdir(data_folder)):
        if file_key in file:
            path = os.path.join(data_folder, file)
            logger.debug("Load from file: %s" % path)
            return path
    raise ValueError("No file was found with key string: %s, in filename", file_key)


def from_csv(pathtocsv: str) -> pd.DataFrame:
    """
    Loading data from csv.

    Parameters
    ----------
    pathtocsv:  path to csv file

    Return
    ----------
    Loaded data in the format of pd.DataFrame.
    """
    try:
        df = pd.read_excel(pathtocsv, engine='xlrd')
    except OSError:
        logging.error("csv file importing failed.")
        exit(1)
    logging.debug("csv file loaded.")
    df = df.drop(['Description'], axis=1)  # no information in Description column

    return df

