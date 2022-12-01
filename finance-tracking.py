import pandas as pd
import os
from pathlib import Path
import yaml
import processing


config_dir = Path(__file__).parent
with open(config_dir.joinpath('config.yaml'), 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)


print("Source data loading -", end=' ')
df = pd.read_excel(os.path.join(Path(__file__).parent,
                                config['INITIAL_DATA']['FOLDER'], config['INITIAL_DATA']['FILE']), engine='xlrd')
df = df.drop(['Description'], axis=1)  # no information in Description column
print("ok")


print("Currencies conversion -", end=' ')
skip_list = ['Transfer', 'Расчеты']
df_conv = processing.currency.convert(df, fromcur='UZS', tocur='KZT', skiplist=skip_list)
df_conv = processing.currency.convert(df_conv, fromcur='KZT', tocur='RUB', skiplist=skip_list)
print("ok")


print("Wallet dynamics calculation -", end=' ')
wallet = processing.Wallet(accounts=list(set(df_conv['Account'])),
                            mindate=df_conv['Date'].min(), maxdate=df_conv['Date'].max())
wallet.load_data(df_conv)
print("ok")


print("Income and expense by months -", end=' ')
min_date = df_conv['Date'].min()
max_date = df_conv['Date'].max()
inc_cat = list(set(df_conv.loc[df_conv['Type'] == 'Income', 'Category']))
income = processing.Balance(catlist=inc_cat, mindate=min_date, maxdate=max_date)
income.load_data(df_conv, typekey='Income')

exp_cat = list(set(df_conv.loc[df_conv['Type'] == 'Expense', 'Category']))
expense = processing.Balance(catlist=exp_cat, mindate=min_date, maxdate=max_date)
expense.load_data(df_conv, typekey='Expense')
print("ok")


print("Export to xsls -", end=' ')
export_file = os.path.join(Path(__file__).parent, config['EXPORT']['FOLDER'], config['EXPORT']['FILE'])
inc_export = processing.Export(income.df)
inc_export.use_template_sort(config['EXPORT']['INCOME_TEMPLATE'], precision=0)

exp_export = processing.Export(expense.df)
exp_export.use_template_sort(config['EXPORT']['EXPENSE_TEMPLATE'], multiply=-1., precision=0)

with pd.ExcelWriter(export_file) as writer:
    inc_export.df.to_excel(writer, sheet_name='Income')
    exp_export.df.to_excel(writer, sheet_name='Expense')
print("ok")


print("Plotting data -", end=' ')
# add income and expense dynamics with averaging in certain window
# add DataFrame to balance
# setting to plot function by dictionary
print("ok")

