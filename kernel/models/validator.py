"""

Custom Datatype and Schema Validators

"""

import datetime
import rfc3987
import re
from kernel.utils import CustomException, Codes
from .db_schema import INTERNAL_FIELDS
from six import string_types


def validate_schema(data, schema, format_checker=True):
    """
        To Validate Schema in given data
    """
    validate(data, schema)


def validate_partial_update_array_params(source_dict, source_schema):
    """
        DO PARTIAL VALIDATION OF Update Keys in $push, $pull, $pullAll,
        $pushAll and $addToSet Operators
    """

    for field in source_dict.keys():
        datatype = None
        field_split = field.split(".")
        field = field_split[0]
        if source_schema.get("properties").get(field):
            datatype = source_schema["properties"][field].get("type")

        if not datatype:
            continue
        if (len(field_split) == 1 and datatype not in ["list", "array"]) or \
                (len(field_split) > 1 and datatype not in ["object"]):
            raise CustomException("%s INVALID TYPE" % field)


def validate_partial_update_set_unset(source_dict, source_schema):
    """
        DO PARTIAL VALIDATION OF Update Keys in $set and $unset Oprators
    """
    for key, value in source_dict.iteritems():
        key_split = key.split(".")
        check_key = key_split[0]

        if value is None or not value:
            if check_key in (source_schema.get("required") or []):
                raise CustomException("%s is a required field" % key)
            continue

        if len(key_split) > 1:
            if source_schema.get("properties").get(check_key).get("type") in \
                    ["object", "array", "list"]:
                continue
            raise CustomException("%s INVALID TYPE" % key)

        try:
            validate_schema(value, source_schema.get("properties", {}).get(key) or INTERNAL_FIELDS.get(key))
        except Exception as e:
            raise CustomException(str(e), Codes.INVALID_PARAM)


def validate_dict(data, schema):
    if not isinstance(data, dict):
        raise Exception('Invalid object type')
    if schema.get('required'):
        required_check(data, schema['required'])
    if schema.get('properties'):
        for k, v in data.items():
            if schema['properties'].get(k):
                try:
                    validate(v, schema['properties'][k])
                except Exception as e:
                    raise TypeError("Invalid {} : {}".format(k, e.message))


def validate_list(data, schema):
    if not isinstance(data, list):
        raise TypeError("arg must be a list, not a {}".format(type(data)))
    if schema.get('item'):
        for item in data:
            validate(item, schema.get('item'))


def validate_string(data, schema):
    if not isinstance(data, string_types):
        raise TypeError("arg must be a string, not a {}".format(type(data)))
    if schema.get('possible_values'):
        check_in_possible_values(data, schema)


def validate_datetime(data, schema):
    if type(data) is not datetime.datetime:
        raise TypeError('arg must be a datetime.datetime, not a %s' % type(data))


def validate_integer(data, schema):
    if not isinstance(data, int):
        raise TypeError("arg must be a integer, not a {}".format(type(data)))
    if schema.get('possible_values'):
        check_in_possible_values(data, schema)


def validate_float(data, schema):
    if not isinstance(data, (int, float)):
        raise TypeError("arg must be a float, not a {}".format(type(data)))


def validate_boolean(data, schema):
    if not isinstance(data, bool):
        raise TypeError("arg must be a boolean, not a {}".format(type(data)))


def required_check(data, required):
    for key in required:
        if data.get(key) is None:
            raise Exception("{} is a required key".format(key))


def check_format(data, schema):
    if schema.get('allOf'):
        for check in schema.get('allOf'):
            check_format(data, check)
    if schema.get('maxLength'):
        maxLength(data, schema.get('maxLength'))
    if schema.get('minLength'):
        minLength(data, schema.get('minLength'))
    if schema.get('format'):
        if FORMAT_CHECKS.get(schema.get('format')):
            FORMAT_CHECKS[schema.get('format')](data)


def check_uri(data):
    if not isinstance(data, str) and not isinstance(data, string_types):
        raise TypeError("URL must be a string, not a {}".format(data))
    try:
        rfc3987.parse(data, rule="URI")
    except Exception as e:
        print(e)
        raise TypeError('except URL type, found {}'.format(data))


def check_email(data):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]{2,}\.[a-zA-Z]{2,}", data):
        raise TypeError("Invalid email format, found {}".format(data))


def check_mobile(data):
    if not re.match(r'^[6-9]\d{9}$', data):
        raise TypeError("Invalid mobile_no format, found {}".format(data))


def max_length(value, key):
    if len(value) > key:
        raise Exception("maxLength is {} : found {} in ({})".format(key, len(value), value))


def min_ength(value, key):
    if len(value) < key:
        raise Exception("minLength is {} : found {} in ({})".format(key, len(value), value))


def check_in_possible_values(data, schema):
    if schema.get('possible_values') and data not in schema['possible_values']:
        raise CustomException("Invalid arg value possible_values are: "
                              + ",".join(map(str, schema['possible_values'])))


FORMAT_CHECKS = {
    'uri': check_uri,
    'email': check_email,
    'mobile': check_mobile,
}

DATA_TYPES = {
    'object': validate_dict,
    'list': validate_list,
    'string': validate_string,
    'datetime': validate_datetime,
    'number': validate_integer,
    'boolean': validate_boolean,
    'float': validate_float,
}


def validate(data, schema):
    if not schema.get('type'):
        raise Exception("Invalid schema")
    _type = schema['type']
    if _type not in DATA_TYPES.keys():
        raise Exception("Invalid Data type: {}".format(_type))
    DATA_TYPES[_type](data, schema)
    check_format(data, schema)
