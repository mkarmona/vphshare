__author__ = 'm.balasso@scsitaly.com, a.saglimbeni@scsitaly.com'


import re
import requests
import xmltodict
from masterinterface.atos.config import *
from exceptions import AtosServiceException
from ordereddict import OrderedDict


def from_dict_to_payload(metadata):

    return "<metadata>%s</metadata>" % "".join(["<%s>%s</%s>" % (key, item, key) for key, item in metadata.items()])


def get_all_resources_metadata():
    """
        return a list of dict with all the resources found into the global catalog
    """
    try:
        response = requests.get(GLOBAL_METADATA_API)

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        metadata = xmltodict.parse(response.text.encode('utf-8'))

        return metadata["resource_metadata_list"]["resource_metadata"]

    except BaseException, e:
        raise AtosServiceException("Error while contacting Atos Service: %s" % e.message)


def set_resource_metadata(metadata):
    """
        given a metadata dictionary create a new entry into the global catalog.
        return the resource global id as a string
    """

    try:
        headers = {'Accept': '*/*', 'content-type': 'application/xml', 'Cache-Control': 'no-cache'}
        response = requests.post(GLOBAL_METADATA_API, data=from_dict_to_payload(metadata), headers=headers)

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        regEx = re.compile('global_id>(.*?)<')

        return regEx.search(response.text).group(1)

    except BaseException, e:
        raise AtosServiceException("Error while contacting Atos Service: %s" % e.message)


def get_resource_metadata(global_id):
    """
        given a resource global id return its metadata as a dictionary
    """
    try:
        response = requests.get(RESOURCE_METADATA_API % global_id)

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        metadata = xmltodict.parse(response.text.encode('utf-8'))

        return metadata['resource_metadata']

    except BaseException, e:
        raise AtosServiceException("Error while contacting Atos Service: %s" % e.message)


def update_resource_metadata(global_id, metadata):
    """
        given a metadata dictionary and a resource global id, update the resource medatada into the global catalog.
        return the resource global id as a string
    """

    try:
        headers = {'Accept': '*/*', 'content-type': 'application/xml', 'Cache-Control': 'no-cache'}
        response = requests.put(RESOURCE_METADATA_API % global_id, data=from_dict_to_payload(metadata), headers=headers)

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        regEx = re.compile('global_id>(.*?)<')

        return regEx.search(response.text).group(1)

    except BaseException, e:
        raise AtosServiceException("Error while contacting Atos Service: %s" % e.message)


def delete_resource_metadata(global_id):
    """
        given a metadata dictionary and a resource global id, update the resource medatada into the global catalog.
        return the resource global id as a string
    """

    try:
        headers = {'Accept': '*/*', 'content-type': 'application/xml', 'Cache-Control': 'no-cache'}
        response = requests.delete(RESOURCE_METADATA_API % global_id, headers=headers)

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        return True

    except BaseException, e:
        raise AtosServiceException("Error while contacting Atos Service: %s" % e.message)


def get_facets():
    """
        return the facets list
    """

    return FACETS_LIST


def filter_resources_by_facet(facet, value):
    """
        given a facet and a value return the list of the resources that match the query
    """

    try:
        response = requests.get(FACETS_METADATA_API % (facet, value))

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        metadata = xmltodict.parse(response.text.encode('utf-8'))
        try:
            return metadata["resource_metadata_list"]['resource_metadata']
        except Exception, e:
            return []

    except BaseException, e:
        raise AtosServiceException("Error while contacting Atos Service: %s" % e.message)


def filter_resources_by_author(author):
    """
    """

    return filter_resources_by_facet('author', author)


def filter_resources_by_type(resource_type):
    """
    """

    return filter_resources_by_facet('type', resource_type)


def filter_resources_by_facets(query):
    """
        given a dictionary query, a list of resources that match all the given condition is returned
    """

    if not type(query) is dict:
        raise TypeError("A dictionary type is required for query parameter")

    resources = filter_resources_by_facet(query.keys()[0], query[query.keys()[0]])

    del query[query.keys()[0]]

    for facet, value in query.items():
        for resource in resources:
            if not facet in resource or not resource[facet].count(value):
                resources.remove(resource)

    return resources


def filter_resources_by_text(text):
    """
    """

    resources = get_all_resources_metadata()

    for resource in resources:
        if not str(resource.items()).count(text):
            resources.remove(resource['resource_metadata'])

    return resources

logicalExpressionBase = '(name:"%s" OR description:"%s")'


def filter_resources_by_expression(expression):
    """

    """
    logicalExpression = logicalExpressionBase % (expression['search_text'], expression['search_text'])
    for key, values in expression.items():
        if type(values) is list and len(values) > 0:
            logicalExpression += '('
            for value in values:
                logicalExpression += ' %s="%s" OR' % (key, value)
            logicalExpression = logicalExpression[:-2]
            logicalExpression += ') AND '

    try:
        response = requests.get(FILTER_METADATA_API % logicalExpression)

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        resources = xmltodict.parse(response.text.encode('utf-8'))["resource_metadata_list"]["resource_metadata"]
        if type(resources) is dict:
            resources = [resources]
        results = OrderedDict()
        for resource in resources:
            position = str(resource.values()).count(expression['search_text'])

            if position not in results:
                results[position] = []
            results[position].append(resource)

        keys = results.keys()
        keys.sort(reverse=True)
        resources = []
        countType = {}
        for key in keys:
            for resource in results[key]:
                if resource['type'] not in countType:
                    countType[resource['type']] = 0
                countType[resource['type']] += 1
                resources.append(resource)

        return resources, countType

    except BaseException, e:
        return [],{}


def search_resource(text, filters = {}):

    try:
        request_url = SEARCH_METADATA_API % (text, text)
        filters_expressions = []
        for key, values in filters.items():
            if type(values) is list and len(values) > 0:
                filter_expression = []
                for value in values:
                    filter_expression.append("%s:%s" % (key, value))

                filters_expressions.append("(%s)" % " OR ".join(filter_expression))

        if len(filters_expressions):
            response = requests.get(request_url + " AND " + " AND ".join(filters_expressions))
        else:
            response = requests.get(request_url)

        if response.status_code != 200:
            raise AtosServiceException("Error while contacting Atos Service: status code = %s" % response.status_code)

        resources = xmltodict.parse(response.text.encode('utf-8'))["resource_metadata_list"]["resource_metadata"]
        countType = {'Dataset': 0, 'Workflow': 0, 'Atomic Service': 0, 'File': 0, 'SWS': 0, 'Application': 0}
        if type(resources) is dict:
            resources = [resources]

        for resource in resources:
            if resource['type'] not in countType and 'Other' not in countType:
                countType['Other'] = 0
            if resource['type'] not in countType and 'Other' in countType:
                countType['Other'] += 1
                continue
            countType[resource['type']] += 1

        return resources, countType

    except BaseException, e:
        return [], {}
