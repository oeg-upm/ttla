from loader import *
import os
import sys
import pandas as pd
import numpy as np
from commons import meta_dir, data_dir, proj_path
from label import classification
import logging
from commons.logger import set_config
logger = set_config(logging.getLogger(__name__))
np.set_printoptions(suppress=True)

meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')


def get_processed_files(fdir):
    """
    get processed files
    :return:
    """
    processed = []
    df = pd.read_csv(fdir, sep='\t')
    for idx, row in df.iterrows():
        processed.append(row['fname'])
    return processed


def write_header_if_not(fdir):
    """
    :param fdir:
    :return:
    """
    header = 'fname\tmembership\tk\tproperty_uri\n'
    if not os.path.isfile(fdir):
        f = open(fdir, 'w')
        f.write(header)
        f.close()
    else:
        f = open(fdir)
        content = f.read()
        if content.strip() == '':
            f.close()
            f = open(fdir, 'w')
            f.write(header)
        f.close()


def append_score(fdir, results):
    """
    :param scr:
    :return:
    """
    f = open(fdir,'a')
    f.write(results+"\n")
    f.close()


def get_column(fname, column_id):
    """
    :param fname:
    :param column_id:
    :return:
    """
    logger.debug("get values for file: %s column %d" % (fname, column_id))
    fdir = os.path.join(data_dir, 'T2Dv2', fname+".csv")
    df = pd.read_csv(fdir)
    col_name = df.columns.values[column_id]
    return list(df[col_name])


def label_experiment():
    """
    Run the experiment for web commons
    :return:
    """
    scores_fname = "web_commons_v2_scores.tsv"
    scores_file = os.path.join(proj_path, 'experiments', scores_fname)
    write_header_if_not(scores_file)
    processed_files = get_processed_files(scores_file)
    logger.debug("%d processed files: " % len(processed_files))
    df = pd.read_csv(meta_file_dir)
    # print(df.columns.values)
    for idx, row in df.iterrows():
        if row['columnid'] == '' or pd.isna(row['columnid']):# is np.nan:
            continue
        if row['filename'] in processed_files:
            continue
        class_uri = "http://dbpedia.org/ontology/"+row['concept']
        if row['kind'] == commons.ORDINAL:
            kind = row['kind']
        else:
            kind = row['sub_kind']
        # print("<"+str(row['columnid'])+">  "+str(type(row['columnid'])))
        logger.debug("get column from file: "+row['filename'])
        col = get_column(row['filename'], int(row['columnid']))
        logger.debug("classify: kind: %s , class: %s" % (kind, class_uri))
        predictions = classification.classify(kind=kind, class_uri=class_uri, columns=[col])
        for pred in predictions:
            # for pair in pred:
            for idx, pair in enumerate(pred):
                append_score(scores_file, "\t".join([row['filename']+".csv", str(idx+1), str(pair[0]), str(pair[1])]))


def print_help():
    help_msg = """
    TASK:
        detect
        label
    python web_commons_v2.py TASK

    """
    print(help_msg)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "detect":
            pass
        elif sys.argv[1] == "label":
            label_experiment()
        else:
            print_help()
    else:
        print_help()