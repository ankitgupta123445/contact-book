def query_list(key, val, query):
    if not isinstance(val, list):
        val = [val]
    query[key] = {'$in': val}
    return query


def query_string(key, val, query):
    query[key] = val
    return query


def get_web_query(web_id, query={}, published_required=True):
    query = query_string("web.url", web_id, query)

    if published_required:
        query = query_string("published_status", "published", query)

    return query


def get_id_query(_id, query={}, published_required=True):
    query = query_list("_id", _id, query)
    if published_required:
        query = query_string("published_status", "published", query)
    return query


class Query(object):

    def __init__(self, query={}):
        self.query = {}

    def equal(self, field, value=None, is_boolean=False):
        if value or is_boolean:
            self.query[field] = {'$in': value} if isinstance(value, list) else value

    def op(self, op, field, value=None):
        if not value:
            return
        if not self.query.get(field):
            self.query[field] = {op: value}
        else:
            self.query[field][op] = value


class Update(object):

    def __init__(self, update={}):
        self.update = {}

    def op(self, op, field, value=None, allow_null=False):
        if not value and not allow_null and not isinstance(value, bool):
            return
        if not self.update.get(op):
            self.update[op] = {field: value}
        else:
            self.update[op][field] = value
