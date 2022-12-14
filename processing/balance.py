import logging
import pandas as pd
from typing import List


logger = logging.getLogger(__name__)
logger.info("Loaded %s module." % __name__)


class Balance:
    """
    Class for analysing of income or expense by categories.
    """
    def __init__(self, catlist: List[str], mindate: str, maxdate: str) -> None:
        """
        Preparing data for calculations by categories.

        Parameters
        ----------
        catlist: list of categories
        mindate: string with minimum of date range
        maxdate: string with maximum of date range
        """
        max_date = pd.to_datetime(str(maxdate.year) + '-' + str(maxdate.month + 1) + '-1')
        ind = pd.date_range(start=mindate, end=max_date, freq='M').to_period('M')
        self.df = pd.DataFrame([[0 for cat in catlist] for month in ind], index=ind, columns=catlist)
        logger.debug("Month periods were initialized and set as index.")

    def load_data(self, data: pd.DataFrame, typekey: str) -> pd.DataFrame:
        """
        Processing data by categories.

        Parameters
        ----------
        data:    pd.DataFrame of source data for processing by categories
        typekey: key for processing current type: Income or Expense
        """
        data.index = data.set_index('Date').index.to_period('M')
        logger.debug("Index is converted to month periods.")
        for month in self.df.index:
            df_cat_M = data.loc[(data['Type'] == typekey) & (data.index == month)]
            for cat in self.df.columns:
                self.df.loc[month, cat] += df_cat_M.loc[df_cat_M['Category'] == cat, 'Amount'].sum()
        logger.debug("Data")

