import pandas as pd
import os
from pathlib import Path
import yaml
import processing

config_dir = Path(__file__).parent
with open(config_dir.joinpath('config.yaml')) as config_file:
    config = yaml.safe_load(config_file)

# load data from xls file
df = pd.read_excel(os.path.join(Path(__file__).parent, config['DATA_FOLDER'], config['DATA_FILE']),
                   engine='xlrd')
df = df.drop(['Description'], axis=1)  # no information in Description column
# df.Date = pd.to_datetime(df.Date).dt.date  # remove HH:MM:SS

# currencies conversion
basic_curr = 'RUB'
skip_list = ['Transfer', 'Расчеты']
df_conv = processing.currency.convert(df, fromcur='UZS', tocur='KZT', skiplist=skip_list)
df_conv = processing.currency.convert(df_conv, fromcur='KZT', tocur=basic_curr, skiplist=skip_list)

wallets = processing.Wallet(accounts=list(set(df['Account'])), min_date=df['Date'].min(), max_date=df['Date'].max())
wallets.load_data(df_conv)

print('ok')
