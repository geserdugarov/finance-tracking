import os
import yaml
import processing
import logging
import config_log
import pandas as pd
import pathlib


config_dir = pathlib.Path(__file__).parent
with open(config_dir.joinpath('config.yaml'), 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)


if __name__ == '__main__':
    filepath = processing.load.find_file(data_folder=os.path.join(config_dir, config['DATA']['FOLDER']),
                                         file_key=config['DATA']['FILE_PATTERN'])
    df = processing.load.from_csv(pathtocsv=filepath)
    logging.info("Source data loading - finished.")

    min_date_df = df['Date'].min()
    max_date_df = df['Date'].max()

    skip_list = ['Transfer', 'Расчеты']
    df_conv = processing.currency.convert(df, fromcur='UZS', tocur='KZT', skiplist=skip_list)
    logging.info("Currencies conversion from UZS to KZT - finished.")
    df_conv = processing.currency.convert(df_conv, fromcur='KZT', tocur='RUB', skiplist=skip_list)
    logging.info("Currencies conversion from KZT to RUB - finished.")

    inc_cat = list(set(df_conv.loc[df_conv['Type'] == 'Income', 'Category']))
    income = processing.Balance(catlist=inc_cat, mindate=min_date_df, maxdate=max_date_df)
    income.load_data(df_conv, typekey='Income')
    logging.info("Income analysis by categories - finished.")

    exp_cat = list(set(df_conv.loc[df_conv['Type'] == 'Expense', 'Category']))
    expense = processing.Balance(catlist=exp_cat, mindate=min_date_df, maxdate=max_date_df)
    expense.load_data(df_conv, typekey='Expense')
    logging.info("Expense analysis by categories - finished.")

    file_export = os.path.join(pathlib.Path(__file__).parent, config['EXPORT']['FOLDER'], config['EXPORT']['FILE'])
    inc_export = processing.export.sort_by_template(data=income.df, template=config['EXPORT']['INCOME_TEMPLATE'])
    logging.debug("Income data for export prepared.")
    exp_export = processing.export.sort_by_template(data=expense.df, template=config['EXPORT']['EXPENSE_TEMPLATE'])
    logging.debug("Expense data for export prepared.")

    with pd.ExcelWriter(file_export) as writer:
        round(inc_export, 0).to_excel(writer, sheet_name='Income')
        round(-exp_export, 0).to_excel(writer, sheet_name='Expense')
    logging.info("Export to xsls - finished.")

    wallet = processing.Wallet(accounts=list(set(df_conv['Account'])),
                               mindate=df_conv['Date'].min(), maxdate=df_conv['Date'].max())
    wallet.load_data(df_conv)
    logging.info("Wallet dynamics processed - finished.")

    # logging.info("Plotting data - started")
    # add income and expense dynamics with averaging in certain window
    # add DataFrame to balance
    # setting to plot function by dictionary
    # logging.info("Plotting data - finished")

