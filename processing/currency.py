import pandas as pd


def convert(data: pd.DataFrame, fromcur: str, tocur: str, skiplist: list) -> pd.DataFrame:
    data_conv = data.copy(deep=True)
    courses = _collect_courses(data_conv, fromcur=fromcur, tocur=tocur, skiplist=skiplist)
    ind = data_conv.loc[data_conv['Currency'] == fromcur].index
    courses_ind = courses.set_index('Date').index.get_indexer(data_conv.loc[ind]['Date'], method='nearest')
    for i, ci in zip(ind, courses_ind):
        data_conv.loc[i, 'Amount'] = data_conv.loc[i, 'Amount'] * courses.loc[courses_ind[ci], 'Course']
        data_conv.loc[i, 'Currency'] = tocur

    return data_conv


def _collect_courses(data: pd.DataFrame, fromcur: str, tocur: str, skiplist: list) -> pd.DataFrame:
    transfers = data.loc[data['Type'] == 'Transfer']
    tf = transfers.loc[transfers['Currency'] == fromcur]
    tf = tf.loc[~tf['Name'].isin(skiplist)]
    tf_ids = tf.index

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

    # if there were more than 1 exchanges, leave last only
    return cources.drop_duplicates(subset=['Date'])

