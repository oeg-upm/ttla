import os
import pandas as pd

proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

data_dir = os.path.join(proj_path, 'data')
meta_dir = os.path.join(proj_path, 'meta')

# kinds
NOMINAL = "nominal"
ORDINAL = "ordinal"
RATIO_INTERVAL = "ratio-interval"

# sub kinds
CATEGORICAL = "categorical"
SEQUENTIAL = "sequential"
RANDOM = "random"
COUNTS = "counts"
OTHER = "other"


# I am not sure of the below is useful
# kinds and subkinds
KINDS = {
    ORDINAL: [""],
    NOMINAL: [CATEGORICAL, SEQUENTIAL, RANDOM],
    RATIO_INTERVAL: [COUNTS, OTHER],
}


def t2dv2_columns_of_kind(num_kind, sub_kind=None):
    """
    :param num_kind: nominal, ordinal, ratio-interval
    :return: a dataframe of the specified kind
    """
    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
    if sub_kind is None:
        dfkind = df[df.kind==num_kind]
    else:
        dfkind = df[df.kind == num_kind and df.sub_kind == sub_kind]
    print(dfkind)
    return dfkind