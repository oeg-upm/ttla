from experiments.loader import *
import os
import sys
import pandas as pd
import numpy as np
from pprint import PrettyPrinter
from commons import meta_dir, data_dir, proj_path
from label import classification
from detect.testDetection import type_evaluation
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
        df_results.loc[index, 'kind'] = kind
        df_results.loc[index, 'sub_kind'] = sub_kind

    print(df_results)
    df_results.to_csv(results_with_kinds_fdir, sep="\t")


def compute_score_from_df(kind, df, is_sub, k):
    """
    :param kind:
    :param df:
    :return:
    """
    if is_sub is None:
        df_kind = df
    elif is_sub:
        if kind == commons.OTHER:
            df_kind = df[df.sub_kind.isin([commons.OTHER,commons.RANDOM])]
        elif kind == commons.RANDOM:
            return {}
        else:
            df_kind = df[df.sub_kind == kind]
    else:
        df_kind = df[df.kind == kind]

    df_found = df_kind[df_kind.k > 0]
    df_correct = df_found[df_found.k <= k]
    df_notfound = df_kind[df_kind.k == 0]

    #
    # df_k = df_kind[df_kind.k <= k]
    # df_rec = df_kind[df_kind.k != 0]
    if df_kind.shape[0] == 0:
        prec = "N/A"
        rec = "N/A"
        f1 = "N/A"
    else:
        prec = df_correct.shape[0] * 1.0 / (df_found.shape[0] * 1.0)
        # prec = df_k.shape[0]*1.0/df_kind.shape[0]
        rec = df_correct.shape[0] * 1.0 / (df_notfound.shape[0] + df_correct.shape[0] * 1.0)
        # rec = df_rec.shape[0]*1.0/df_kind.shape[0]
        f1 = 2 * prec * rec / (prec+rec)
        prec = str(round(prec, 3))
        rec = str(round(rec, 3))
        f1 = str(round(f1, 3))
    d = {
        "precision": prec,
        "recall": rec,
        "f1": f1,
    }
    return d
    # return prec


def show_scores_from_results():
    results_with_kinds_fdir = os.path.join(proj_path, 'experiments', 'web_commons_v2_results.tsv')
    df = pd.read_csv(results_with_kinds_fdir, sep='\t')
    scores = {
        1: {},
        3: {},
        5: {},
        10: {}
    }
    for k in scores.keys():
        for kind in commons.KINDS:
            if commons.KINDS[kind] == []:
                scores[k][kind] = compute_score_from_df(kind=kind, df=df, is_sub=False, k=k)
            else:
                for sub in commons.KINDS[kind]:
                    scores[k][sub] = compute_score_from_df(kind=sub, df=df, is_sub=True, k=k)
            scores[k]["all"] = compute_score_from_df(kind="all", df=df, is_sub=None, k=k)
        del scores[k][commons.RANDOM]
        del scores[k][commons.YEAR]

    pp = PrettyPrinter(indent=2)
    pp.pprint(scores)
    return scores
    #
    # print scores


def print_help():
    help_msg = """
    TASK:
        detect
        label
        addkinds
        scores
        
    python web_commons_v2.py TASK

    """
    print(help_msg)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "detect":
            type_evaluation()
        elif sys.argv[1] == "label":
            label_experiment()
        elif sys.argv[1] == "addkinds":
            add_kind_to_results()
        elif sys.argv[1] == "scores":
            show_scores_from_results()
        else:
            print_help()
    else:
        print_help()