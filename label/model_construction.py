import commons
import detect
from features import compute_features
import os

import logging
from commons.logger import set_config
logger = set_config(logging.getLogger(__name__))


ENDPOINT = commons.ENDPOINT
TEST = False


def get_features_and_kinds(class_uri):
    """
    :param class_uri:
    :return:
    """
    fk_pairs = []
    logger.debug("ask for properties")
    properties = commons.get_properties(class_uri=class_uri, endpoint=ENDPOINT)
    logger.debug("properties: "+str(len(properties)))
    for p in properties:
        logger.debug("objects for property: "+p)
        values = commons.get_objects(endpoint=ENDPOINT, class_uri=class_uri, property_uri=p)
        logger.debug("got %d objects" % len(values))
        nums = commons.get_numerics_from_list(values)
        if nums and len(nums) > commons.MIN_NUM_NUMS:
            logger.debug("%d of them are nums" % len(nums))
            kind = detect.get_num_kind(nums)
            logger.debug("detect kind: "+kind)
            features = compute_features(kind=kind, nums=nums)
            if features is None:
                logger.debug("No features")
                continue
            logger.debug("computed features: "+str(features))
            pair = {
                'kind': kind,
                'features': features,
                'property_uri': p,
            }
            fk_pairs.append(pair)
        # else:
        #     logger.debug("no enough nums: "+str(nums))
    return fk_pairs


def build_model(class_uri):
    """
    :param class_uri:
    :return: the directory of the model
    """
    logger.debug("class uri: "+class_uri)
    fname = commons.class_uri_to_fname(class_uri=class_uri)
    logger.debug("fname: "+fname)
    model_fdir = os.path.join(commons.models_dir, fname)+'.tsv'
    if TEST:
        model_fdir += '.test'
        f = open(model_fdir, 'w')
        f.close()
        os.remove(model_fdir)

    logger.debug("model_fdir: "+model_fdir)
    if os.path.isfile(model_fdir):
        logger.debug("Model already exists")
        return model_fdir

    features_and_kinds = get_features_and_kinds(class_uri=class_uri)
    model_txt = ""
    logger.debug("num of features and kinds: %d" % (len(features_and_kinds)))
    for fk in features_and_kinds:
        features_txt = ",".join([str(f) for f in fk['features']])
        line = "%s\t%s\t%s\n" % (fk['property_uri'], fk['kind'], features_txt)
        model_txt+=line
    f = open(model_fdir, 'w')
    f.write(model_txt)
    f.close()
    return model_fdir

