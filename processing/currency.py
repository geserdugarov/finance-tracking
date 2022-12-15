import logging
import pandas as pd
from typing import List


logger = logging.getLogger(__name__)
logger.info("Loaded %s module." % __name__)


def convert(data: pd.DataFrame, fromcur: str, tocur: str, skiplist: List[str]) -> pd.DataFrame:
    """
    Transactions conversion from one currency to another.

    Parameters
    ----------
    data:     pd.DataFrame of incomes, expenses, or transitions
    fromcur:  currency, that should be converted
    tocur:    currency, to which transactions should be converted
    skiplist: list of transaction names, which should be skipped

    Return
    ----------
    Converted data with similar structure with 'data'.
    """
    data_conv = data.copy(deep=True)
    logger.debug("Transactions copied for conversion.")
    courses = _collect_courses(data_conv, fromcur=fromcur, tocur=tocur, skiplist=skiplist)
    logger.debug("Courses for conversions were estimated.")
    ind = data_conv.loc[data_conv['Currency'] == fromcur].index
    courses_ind = courses.set_index('Date').index.get_indexer(data_conv.loc[ind]['Date'], method='nearest')
    for i, ci in zip(ind, courses_ind):
        data_conv.loc[i, 'Amount'] = data_conv.loc[i, 'Amount'] * courses.loc[courses_ind[ci], 'Course']
        data_conv.loc[i, 'Currency'] = tocur
    logger.debug("Conversions were completed.")

    return data_conv


def _collect_courses(data: pd.DataFrame, fromcur: str, tocur: str, skiplist: list) -> pd.DataFrame:
    """
    Internal function for courses estimation between 'fromcur' and 'tocur' currencies.

    Parameters
    ----------
    data:     pd.DataFrame of incomes, expenses, or transitions
    fromcur:  currency, that should be converted
    tocur:    currency, to which transactions should be converted
    skiplist: list of transaction names, which should be skipped

    Return
    ----------
    Courses of exchange from transactions in the format of pd.DataFrame.
    """
    transfers = data.loc[data['Type'] == 'Transfer']
    tf = transfers.loc[transfers['Currency'] == fromcur]
    tf = tf.loc[~tf['Name'].isin(skiplist)]
    tf_ids = tf.index
    logger.debug("Prepared transactions for searching of pairs, which are in fact conversions of currencies.")

    # find pairs of transfers
    cources = pd.DataFrame({'Date': [], 'Course': []})
    for i in tf_ids:
        if i-1 in transfers.index:
            if transfers.loc[i-1, 'Name'] == transfers.loc[i, 'Name'] and transfers.loc[i-1, 'Currency'] == tocur:
                cources.loc[len(cources.index)] = {'Date': transfers.loc[i, 'Date'],
                                                   'Course': -transfers.loc[i-1, 'Amount']/transfers.loc[i, 'Amount'],
                                                   'ID': len(cources.index)}
        if i+1 in transfers.index:
            if transfers.loc[i+1, 'Name'] == transfers.loc[i, 'Name'] and transfers.loc[i+1, 'Currency'] == tocur:
                cources.loc[len(cources.index)] = {'Date': transfers.loc[i, 'Date'],
                                                   'Course': -transfers.loc[i+1, 'Amount']/transfers.loc[i, 'Amount'],
                                                   'ID': len(cources.index)}
    logger.debug("Completed searching of transactions pairs (conversions of currencies).")

    # if there were more than 1 exchanges, leave last only
    return cources.drop_duplicates(subset=['Date'])

