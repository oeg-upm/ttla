import os
import pandas as pd

proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

data_dir = os.path.join(proj_path, 'data')
meta_dir = os.path.join(proj_path, 'meta')


def t2dv2_columns_of_kind(num_kind):
    """
    :param num_kind: nominal, ordinal, ratio-interval
    :return: a dataframe of the specified kind
    """
    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
    dfkind = df[df.kind==num_kind]
    return dfkind