import collections


def convert(data):
    """ Convert dict in unicode to dict in str.
    """
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def getWholeName(domain_name, node_name):
    return "%s_%s" % (domain_name, node_name)


def splitWholeName(frontEndName):
    return frontEndName.split("_")[:2]
