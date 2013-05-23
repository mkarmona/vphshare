from django import template
from datetime import datetime
from permissions.utils import has_local_role
# get a register Library instance
register = template.Library()


def basepath(path):
    base = str(path).split('/')[1]
    return base


def breadcrumbs(path):
    base = '/'
    crumbs = []
    for crumb in str(path).split('/'):
        if not crumb:
            # skip empty
            continue
        current = "%s%s/" % (base, crumb)
        crumbs.append(dict(name=crumb, url=current))
        base = current
    return crumbs


def split(string, sep=" "):
    if string is not None:
        return str(string).split(sep)
    return []


def strTodate(date):
    return datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f')

@register.filter
def strCut(string, lenght):
    if len(string) > int(lenght):
        return string[:int(lenght)] + '....'
    return string

@register.filter
def keyvalue(dict, key):
    if key in dict:
        return dict[key]
    return '0'


def can_read(user, resource):
    # TODO check permissions rather than roles!
    return has_local_role(user, 'Reader', resource) or has_local_role(user, 'Editor', resource) or has_local_role(user, 'Manager', resource) or has_local_role(user, 'Owner', resource)


# register filters
register.filter('breadcrumbs', breadcrumbs)
register.filter('basepath', basepath)
register.filter('split', split)
register.filter('strTodate', strTodate)
register.filter('can_read',can_read)
