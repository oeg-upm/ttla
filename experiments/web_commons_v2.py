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
    header = 'fname\tk\tmembership\tproperty_uri\tcolumn_id\n'
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
    df = df[df.columnid.notnull()]
    logger.debug("shape: "+str(df.shape))
    # print(df.columns.values)
    tottt = 0
    for idx, row in df.iterrows():
        tottt += 1
        logger.debug("tottt: " + str(tottt))
        # if row['columnid'] == '' or pd.isna(row['columnid']):# is np.nan:
        #     continue
        if row['filename'] in processed_files:
            continue
        class_uri = "http://dbpedia.org/ontology/"+row['concept']
        if row['kind'] == commons.ORDINAL:
            kind = row['kind']
        elif row['kind'] == commons.YEAR:  # will ignore the year for now
            logger.debug("ignore year")
            continue
        elif row['sub_kind'] == commons.RANDOM:
            kind = commons.OTHER
        else:
            kind = row['sub_kind']
        logger.debug("not year: "+str(kind))
        # print("<"+str(row['columnid'])+">  "+str(type(row['columnid'])))
        logger.debug("get column from file: "+row['filename'])
        col = get_column(row['filename'], int(row['columnid']))
        logger.debug("classify: kind: %s , class: %s" % (kind, class_uri))
        predictions = classification.classify(kind=kind, class_uri=class_uri, columns=[col])
        for pred in predictions:
            # for pair in pred:
            for idx, pair in enumerate(pred):
                append_score(scores_file, "\t".join([row['filename']+".csv", str(idx+1), str(pair[0]), str(pair[1]), str(row['columnid'])]))


def add_kind_to_results():
    """
    This is to add types from the meta to the results file
    :return:
    """
    results_fdir = os.path.join(proj_path, 'experiments', 'web_commons_v2_scores_results.tsv')
    results_with_kinds_fdir = os.path.join(proj_path, 'experiments', 'web_commons_v2_results.tsv')
    df_results = pd.read_csv(results_fdir, sep='\t')
    df_meta = pd.read_csv(meta_file_dir)
    for index, row in df_results.iterrows():
        df_meta_row = df_meta[df_meta.filename==row['fname'][:-4]][ df_meta.columnid == row['column_id']]
        kind = list(df_meta_row['kind'])[0]
        sub_kind = list(df_meta_row['sub_kind'])[0]
        df_results.loc[index,'kind'] = kind
        df_results.loc[index,'sub_kind'] = sub_kind

    print df_results
    df_results.to_csv(results_with_kinds_fdir, sep="\t")


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
        elif sys.argv[1] == "addkinds":
            add_kind_to_results()
        else:
            print_help()
    else:
        print_help()