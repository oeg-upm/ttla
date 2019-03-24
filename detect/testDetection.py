from loader import *
import os
import pandas as pd
import math
from commons import get_num

from Detection import get_num_kind, get_kind_and_nums
from Detection import Detection


proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
data_dir = os.path.join(proj_path, 'data')
meta_dir = os.path.join(proj_path, 'meta')


def get_numerics_from_list(nums_str_list):
    """
    :param nums_str_list: list of string or numbers or a mix
    :return: list of numbers or None if less than 50% are numbers
    """
    nums = []
    for c in nums_str_list:
        n = get_num(c)
        if n is not None and not math.isnan(n):
            nums.append(n)
    if len(nums) < len(nums_str_list)/2:
        return None
    return nums


# def get_num(num_or_str):
#     """
#     :param num_or_str:
#     :return: number or None if it is not a number
#     """
#     if isinstance(num_or_str, (int, float)):
#         return num_or_str
#     elif isinstance(num_or_str, basestring):
#         if '.' in num_or_str or ',' in num_or_str or num_or_str.isdigit():
#             try:
#                 return float(num_or_str.replace(',', ''))
#             except Exception as e:
#                 return None


def get_column_type(filename, columnid):
    column_type = 'unknown'
    file_path = os.path.join(data_dir, 'T2Dv2',filename+ '.csv')
    #file_path = os.path.join(data_dir, 'T2Dv2/') +filename+ '.csv'
    dftestfile = pd.read_csv(file_path)
    values = dftestfile.iloc[ : , int(columnid) ]

    numbers_list = get_numerics_from_list(values)

    if numbers_list != None:
        column_type = get_num_kind(numbers_list)
    del dftestfile
    return column_type


def overall_evaluation():
    count_successful = 0
    count_failed = 0
    count_overall = 0
    count_year_failed = 0
    count_year_successful = 0
    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
    for index, row in df.iterrows():
        if not math.isnan(row['columnid']):
            #if row['filename'] == '1146722_1_7558140036342906956.tar.gz':
            count_overall += 1
            detected_type = get_column_type(row['filename'], row['columnid'])
            if detected_type == row['kind'] or detected_type == row['sub_kind']:
                count_successful += 1
                if detected_type == 'year':
                    count_year_successful += 1
            else:
                if row['kind'] == 'year' or row['sub_kind'] == 'year':
                    #print("%s | %s | %s - %s / %s" % (row['filename'], row['columnid'], detected_type, row['kind'], row['sub_kind']))
                    count_year_failed += 1
                else:
                    print("%s | %s | %s - %s / %s" % (row['filename'], row['columnid'], detected_type, row['kind'], row['sub_kind']))

                    count_failed += 1
                #print("%s | %s | %s - %s / %s" % (row['filename'], row['columnid'], detected_type, row['kind'], row['sub_kind']))

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("successfully matched: " + str(count_successful))
    print("unsuccessfully matched: " + str(count_failed))

    print("failed year: " + str(count_year_failed))
    print("success year: " + str(count_year_successful))


    print("Overall attempts couter: " + str(count_overall))


def type_evaluation():
    # "nominal", "ratio-interval"
    numerical_types = ["ordinal", "categorical", "sequential", "hierarchical", "random", "count", "other", "year"]
    count_types = {}

    for nt in numerical_types:
        count_types[nt] = {'success': 0, 'failure': 0}

    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
    for index, row in df.iterrows():
        if not math.isnan(row['columnid']):
            detected_type = get_column_type(row['filename'], row['columnid'])
            if detected_type == row['kind'] or detected_type == row['sub_kind']:
                count_types[detected_type]['success'] += 1
            else:
                if row['kind'] in count_types:
                    count_types[row['kind']]['failure'] += 1
                else:
                    count_types[row['sub_kind']]['failure'] += 1


    for key, value in count_types.items():
        print(key + ": " + str(value['success']) + " correct out of " + str(value['failure']+value['success']))

type_evaluation()
