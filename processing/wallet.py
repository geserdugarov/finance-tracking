import pandas as pd


class Wallet:
    def __init__(self, accounts: list, mindate: str, maxdate: str) -> None:
        dates = pd.date_range(start=mindate, end=maxdate, freq='D')
        self.df = pd.DataFrame([[0 for acc in accounts] for date in dates],
                               index=dates,
                               columns=accounts)

    def load_data(self, data: pd.DataFrame) -> None:
        for day in self.df.index:
            df_day = data.loc[(data['Date'] > day - pd.Timedelta(days=1)) & (data['Date'] <= day)]
            for acc in self.df.columns:
                self.df.loc[day, acc] += df_day.loc[df_day['Account'] == acc, 'Amount'].sum()
        self.df = self.df.cumsum()
