import pandas as pd


class Balance:
    def __init__(self, catlist: list, mindate: str, maxdate: str) -> None:
        max_date = pd.to_datetime(str(maxdate.year) + '-' + str(maxdate.month + 1) + '-1')
        ind = pd.date_range(start=mindate, end=max_date, freq='M').to_period('M')
        self.df = pd.DataFrame([[0 for cat in catlist] for month in ind], index=ind, columns=catlist)

    def load_data(self, data: pd.DataFrame, typekey: str) -> pd.DataFrame:
        for i in range(len(self.df.index)-1):
            month = self.df.index[i]
            data.index = data.set_index('Date').index.to_period('M')
            df_cat_M = data.loc[(data['Type'] == typekey) & (data.index == month)]
            for cat in self.df.columns:
                self.df.loc[month, cat] += df_cat_M.loc[df_cat_M['Category'] == cat, 'Amount'].sum()

