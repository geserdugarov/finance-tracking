import logging
import pandas as pd
from typing import List


logger = logging.getLogger(__name__)
logger.info("Loaded %s module." % __name__)


class Wallet:
    """
    Class for data with dynamic data of wallets balance.
    """
    def __init__(self, accounts: List[str], mindate: str, maxdate: str) -> None:
        """
        Wallets initialization.

        Parameters
        ----------
        accounts: list of wallets names
        mindate:  string with minimum of date range
        maxdate:  string with maximum of date range
        """
        dates = pd.date_range(start=mindate, end=maxdate, freq='D')
        logger.debug("Dates range was prepared (by days).")
        self.df = pd.DataFrame([[0 for acc in accounts] for date in dates],
                               index=dates,
                               columns=accounts)
        logger.debug("DataFrame in Wallet was initialized.")

    def load_data(self, data: pd.DataFrame) -> None:
        """
        Wallets dynamic change processing

        Parameters
        ----------
        data: pd.DataFrame with transactions
        """
        for day in self.df.index:
            df_day = data.loc[(data['Date'] > day - pd.Timedelta(days=1)) & (data['Date'] <= day)]
            for acc in self.df.columns:
                self.df.loc[day, acc] += df_day.loc[df_day['Account'] == acc, 'Amount'].sum()
        logger.debug("Finished processing of wallets dynamic change within days.")
        self.df = self.df.cumsum()
        logger.debug("Finished transition to stacked dynamic change (day by day).")

