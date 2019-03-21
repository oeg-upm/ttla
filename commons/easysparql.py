from SPARQLWrapper import SPARQLWrapper, JSON
import commons


def get_properties(endpoint, class_uri, min_num):
    """
    :param endpoint:
    :param class_uri:
    :return:
    """

    if class_uri is None:
        print "get_properties> class_uri should not be None"
        raise Exception("class_uri ")
        return []
    class_uri_stripped = get_url_stripped(class_uri)
    query = """
                SELECT ?p (count(distinct ?s) as ?num)
                WHERE {
                    ?s a <%s>.
                    ?s ?p[]
                }
                group by ?p
                order by desc(?num)
            """ % class_uri_stripped
    results = run_query(query=query, endpoint=endpoint)
    properties = [r['p']['value'] for r in results if r['num'] >= min_num]
    return properties


def run_query(query=None, endpoint=None, raiseexception=False):
    """
    :param query: raw SPARQL query
    :param endpoint: endpoint source that hosts the data
    :return: query result as a dict
    """
    if endpoint is None:
        error_msg = "endpoints cannot be None"
        print error_msg
        raise Exception(error_msg)
        return []
    sparql = SPARQLWrapper(endpoint=endpoint)
    sparql.setQuery(query=query)
    sparql.setMethod("POST")
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            return results["results"]["bindings"]
        else:
            print "returns 0 rows"
            print "endpoint: "+endpoint
            print "query: <%s>" % str(query).strip()
            return []
    except Exception as e:
        print "sparql error: $$<%s>$$" % str(e)
        print "query: $$<%s>$$" % str(query)
        # if raiseexception:
        #     raise e
        return []


def get_url_stripped(uri):
    """
    :param uri:  <uri> or uri
    :return: uri
    """
    uri_stripped = uri.strip()
    if uri_stripped[0] == "<":
        uri_stripped = uri_stripped[1:]
    if uri_stripped[-1] == ">":
        uri_stripped = uri_stripped[:-1]
    return uri_stripped