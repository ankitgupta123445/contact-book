"""

MONGODB Data Modelling BaseResource class

"""
from datetime import datetime
from six import string_types
from bson.json_util import dumps
from bson.objectid import ObjectId
from bson.son import SON
from itsdangerous import JSONWebSignatureSerializer

from . import pydb
from . import validator
from kernel import app
from pymongo import ReturnDocument

HASH_GEN = JSONWebSignatureSerializer(app.config['SECRET_KEY'])
db = pydb.get_mongo_db(app.config)


def get_db(obj, rp=0):
    if rp != 0:
        rp = 0
    return db[0][rp][obj._coll_name_]


def apply_default_filter_args(filter_args=None,
                              skip_obj_id=False, check_delete=True):
    q_criteria = {}
    if check_delete:
        q_criteria = {'is_deleted': {'$ne': True}}  # ignore seed document
    if filter_args:
        q_criteria.update(filter_args)

    try:
        if isinstance(q_criteria, dict) and '_id' in q_criteria:
            if skip_obj_id:
                pass
            elif isinstance(q_criteria['_id'], string_types) and len(q_criteria['_id']) == 24:
                _id = ObjectId(q_criteria['_id'])
                q_criteria['_id'] = _id
            elif isinstance(q_criteria['_id'], dict):
                for op, val in q_criteria['_id'].iteritems():
                    if isinstance(val, string_types) and len(val) == 24:
                        _id = ObjectId(val)
                        q_criteria['_id'][op] = _id
                    elif isinstance(val, list) and \
                            len(val) > 0 and isinstance(val[0], string_types):
                        val = filter(None, val)
                        _ids = [ObjectId(_id) if len(_id) == 24 else _id for _id in val]
                        q_criteria['_id'][op] = _ids
    except Exception as e:
        print(e)
    return q_criteria


class BaseResource(object):

    def __init__(self, coll_name, data):
        data = data if data is not None else {}
        super(BaseResource, self).__init__()
        self.db_coll = get_db(self, 0)
        self._id = data['_id'] if '_id' in data else None
        self.data = data

    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self._id)

    def get_data(self, encoding=None):
        d = dict((k, v) for (k, v) in self.data.items() if k not in self._reserve_fields_)
        if not isinstance(self._id, string_types):
            d['_id'] = str(self._id)
        else:
            d['_id'] = self._id
        if encoding == 'json':
            return dumps(d)
        else:
            return d

    @classmethod
    def get_all(cls, filter_args, fields=[], limit=25, skip=0, sort_by=False,
                raw_cursor=False, skip_obj_id=False, rp=0, check_delete=True):
        _args = apply_default_filter_args(filter_args, skip_obj_id, check_delete)
        if not fields:
            fields = cls._default_fields_ or ['_id']

        _fields = [field for field in fields if field not in cls._reserve_fields_]

        if sort_by:
            db_cursor = get_db(cls, rp).find(_args, projection=_fields).sort(sort_by).skip(int(skip)).limit(int(limit))
        else:
            db_cursor = get_db(cls, rp).find(_args, projection=_fields).skip(int(skip)).limit(int(limit))
        if raw_cursor:
            return db_cursor

        db_docs = [cls(d) for d in db_cursor]
        return db_docs

    @classmethod
    def clone(cls, _id, rp=0):
        res_doc = get_db(cls, rp).find_one(apply_default_filter_args({'_id': _id}))
        if res_doc:
            res_doc.pop('_id')
            new_res_doc = cls(res_doc)
            new_res_doc.insert()
            return new_res_doc

    @classmethod
    def find_one_and_update(cls, filter_args, update_args, fields=[], upsert=False, return_document="after"):
        res = None
        """
        Validate Update Args
        """
        update_document = {}
        for op, value in update_args.iteritems():
            if op in ['$unset', '$set', '$inc']:
                validator.validate_partial_update_set_unset(value, cls._schema_)
                update_document[op] = dict(value)
            elif op in ['$push', '$pushAll', '$pull', '$pullAll', '$addToSet']:
                validator.validate_partial_update_array_params(value, cls._schema_)
                update_document[op] = dict(value)
            else:
                raise Exception("Invalid Update Operator passed.")

        update_document['$set'] = update_document.get('$set', {'last_updated': datetime.utcnow()})

        """
        Prepare Find Args
        """
        _args = apply_default_filter_args(filter_args)

        """
        prepare projection fields
        """
        if not fields:
            fields = cls._default_fields_ or ['_id']

        _fields = [field for field in fields if field not in cls._reserve_fields_]

        """
        Query MongoDB
        """
        res_doc = get_db(cls, 0).find_one_and_update(
            _args,
            update_document,
            projection=fields,
            upsert=upsert,
            return_document=ReturnDocument.BEFORE if return_document == "before" else ReturnDocument.AFTER
        )
        """
        Create db object
        """
        if res_doc:
            res = cls(res_doc)
        return res

    @classmethod
    def get(cls, filter_args, fields=[], check_delete=True, rp=0):
        res = None
        _args = apply_default_filter_args(filter_args, check_delete=check_delete)
        if not fields:
            fields = cls._default_fields_ or ['_id']

        _fields = [field for field in fields if field not in cls._reserve_fields_]

        if isinstance(fields, dict):
            _fields = fields

        res_doc = get_db(cls, rp).find_one(_args, projection=_fields)

        if res_doc:
            res = cls(res_doc)
        return res

    @classmethod
    def remove_all(cls):
        if cls not in (app.config['ALLOW_PURGE'] or []):
            raise Exception('removal from collection not allowed, use delete')
        else:
            get_db(cls, 0).remove()

    def delete(self):
        self.db_coll.update(
            {'_id': self._id},
            {'$set': {'is_deleted': True}})
        self.__delete_ssearch_object__()

    @classmethod
    def delete_all(cls, filter_args):
        if not app.config['ALLOW_BULK_DELETE'] and cls._coll_name_ not in app.config['ALLOW_BULK_DELETE']:
            raise Exception('bulk delete from collection {} not allowed, use delete'.format(cls._coll_name_))
        if filter_args:
            get_db(cls, 0).update(
                apply_default_filter_args(filter_args),
                {'$set': {'is_deleted': True}},
                multi=True)

    @classmethod
    def count(cls, filter_args=None, rp=0):
        _args = apply_default_filter_args(filter_args)
        return get_db(cls, rp).find(_args).count()

    @classmethod
    def distinct(cls, field, filter_args=None, filter_empty=True, rp=0):
        _args = apply_default_filter_args(filter_args)
        dist_list = get_db(cls, rp).find(_args).distinct(field)
        if filter_empty:
            return filter(None, dist_list)
        return dist_list

    @classmethod
    def group_count(cls, group_field, rp=0):
        pipeline = list()
        pipeline.append({"$group": {"_id": "${}".format(group_field), "count": {"$sum": 1}}})
        return get_db(cls, rp).aggregate(pipeline)

    @classmethod
    def aggregate_multi_count(cls, group_field, match=None, data_field=None, limit=None, data_is_array=True, rp=0):
        pipeline = []

        if match:
            pipeline.append({"$match": match})

        if data_field:
            if data_is_array:
                pipeline.append({"$match": {"%s" % data_field: {"$exists": "true"}}})
                pipeline.append({"$unwind": "$%s" % data_field})
            else:
                pipeline.append({"$match": {"%s" % group_field: {"$exists": "true"}}})

        pipeline.append({"$group": {"_id": "$%s" % group_field, "count": {"$sum": 1}}})
        pipeline.append({"$sort": SON([("count", -1)])})
        if limit:
            pipeline.append({"$limit": limit})

        return get_db(cls, rp).aggregate(pipeline)

    @classmethod
    def aggregate(cls, pipeline, rp=0):
        return get_db(cls, rp).aggregate(pipeline)

    def aggregate_count(self, data_field, group_field, limit=3):
        pipeline = [
            {"$match": {'_id': self._id}},
            {"$unwind": "$%s" % data_field},
            {"$group": {"_id": "$%s" % group_field, "count": {"$sum": 1}}},
            {"$sort": SON([("count", -1)])},
            {"$limit": limit}
        ]
        return self.db_coll.aggregate(pipeline)['result']

    def insert(self):
        if self.data:
            validator.validate_schema(self.data, self._schema_)
        data = {**dict(self.data.items()), 'created_on': datetime.utcnow(), 'last_updated': datetime.utcnow()}

        self._id = self.db_coll.insert(data)
        if not isinstance(self._id, string_types):
            return str(self._id)
        return self._id

    @classmethod
    def bulk_insert(cls, data):
        if not isinstance(data, list):
            data = [data]

        bulk = get_db(cls, 0).initialize_unordered_bulk_op()

        for _d in data:
            validator.validate_schema(_d, cls._schema_)
            _d = {**dict(_d.items()), 'created_on': datetime.utcnow(), 'last_updated': datetime.utcnow()}
            bulk.insert(_d)
        bulk.execute()
        return {'inserted': True}

    @classmethod
    def bulk_statement(cls, data, ignore_last_update=False):
        if not isinstance(data, list):
            data = [data]

        bulk = get_db(cls, 0).initialize_unordered_bulk_op()

        for operation in data:
            if operation.get("insert"):
                v = operation.get("insert")
                if not isinstance(v, dict):
                    continue
                validator.validate_schema(v, cls._schema_)
                v = {**dict(v.items()), 'created_on': datetime.utcnow(), 'last_updated': datetime.utcnow()}
                bulk.insert(v)
            elif operation.get("updateOne") or operation.get("update"):
                v = operation.get("updateOne") or operation.get('update') or {}
                if not isinstance(v, dict):
                    continue
                find_args = v.get('find_args')
                update_args = v.get('update_args')
                if find_args and update_args:
                    update_document = {}
                    for op, value in update_args.iteritems():
                        if op in ['$unset', '$set', '$inc']:
                            validator.validate_partial_update_set_unset(
                                value, cls._schema_)
                            update_document[op] = dict(value)
                        elif op in ['$push', '$pushAll', '$pull', '$pullAll', '$addToSet']:
                            validator.validate_partial_update_array_params(
                                value, cls._schema_)
                            update_document[op] = dict(value)
                        else:
                            raise Exception("Invalid Update Operator passed.")
                    update_document['$set'] = update_document.get('$set', {'_last_updated': datetime.utcnow()})
                    if not ignore_last_update:
                        update_document['$set']['last_updated'] = datetime.utcnow()

                    bulk.find(apply_default_filter_args(find_args)).update(update_document)
            elif operation.get('remove'):
                v = operation.get("remove")
                if not isinstance(v, dict):
                    continue
                find_args = v.get('find_args')
                if find_args:
                    bulk.find(apply_default_filter_args(find_args)).update({'$set': {'is_deleted': True}})

        bulk.execute()
        return {'inserted': True}

    def update(self, update_data):
        validator.validate_schema(update_data, self._schema_)
        update_document = dict()
        update_document['$set'] = {**dict(update_data.items()), 'last_updated': datetime.utcnow()}

        self.db_coll.update({'_id': self._id}, update_document)

    def patch_update(self, update_args, ignore_last_update=False):
        update_document = {}
        for op, value in update_args.iteritems():
            if op in ['$unset', '$set', '$inc']:
                validator.validate_partial_update_set_unset(value, self._schema_)
                update_document[op] = dict(value)
            elif op in ['$push', '$pushAll', '$pull', '$pullAll', '$addToSet']:
                validator.validate_partial_update_array_params(value, self._schema_)
                update_document[op] = dict(value)
            else:
                raise Exception("Invalid Update Operator passed.")

        update_document['$set'] = update_document.get('$set', {'_last_updated': datetime.utcnow()})
        if not ignore_last_update:
            update_document['$set']['last_updated'] = datetime.utcnow()

        self.db_coll.update({'_id': self._id}, update_document)

    def update_array_item_increment(self, array_item, field, incr_by):
        """Increment a field in an array item within a document
        Return true if updated an existing item
        """

        update_document = dict()
        update_document['$inc'] = {field: incr_by}
        q_criteria = {'_id': self._id,  **dict(array_item.items())}
        result = self.db_coll.update(q_criteria, update_document)
        return result['updatedExisting']

    def update_array_item(self, array_item, update_args):
        """Update a field in an array item within a document
        Return true if updated an existing item
        """

        update_document = dict()
        update_document['$set'] = update_args
        q_criteria = {'_id': self._id, **dict(array_item.items())}
        result = self.db_coll.update(q_criteria, update_document)
        return result['updatedExisting']

    @classmethod
    def update_all(cls, filter_args, update_args):
        if not isinstance(update_args, dict):
            raise Exception("filter must be dict")

        filter_args = apply_default_filter_args(filter_args)

        update_document = {}
        for op, value in update_args.iteritems():
            if op in ['$unset', '$set', '$inc']:
                validator.validate_partial_update_set_unset(value, cls._schema_)
                update_document[op] = dict(value)
            elif op in ['$push', '$pushAll', '$pull', '$pullAll', '$addToSet']:
                validator.validate_partial_update_array_params(value, cls._schema_)
                update_document[op] = dict(value)
            else:
                raise Exception("Invalid Update Operator passed.")

        update_document['$set'] = update_document.get('$set', {'last_updated': datetime.utcnow()})
        get_db(cls, 0).update(filter_args, update_document, multi=True)
        return "updated"

    def remove(self):
        if not app.config['ALLOW_PURGE']:
            raise Exception('removal from collection not allowed, use delete')
        if not self._id:
            print("cant remove")
        else:
            self.db_coll.remove(self._id)
            self._id = None
