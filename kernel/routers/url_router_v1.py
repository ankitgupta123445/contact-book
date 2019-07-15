"""

Route will map generic URL patterns to appropriate handlers

"""
from flask import request
from functools import wraps
from kernel.route import REGISTERED_ROUTE
from kernel.util.decorators import is_authorized


def fix_arg(f):
    """
    fix array issue

    variable = ['value']   #issue
    variable = 'value'     #required

    Also checks is primary_schema in REGISTERED_ROUTE

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # To Support Token Via Headers
        if request.headers.get('API-Token'):
            kwargs['token'] = request.headers['API-Token']
        new_kwargs = {}
        for x, y in kwargs.items():
            if isinstance(y, list) and len(y) == 1:
                new_kwargs[x] = y[0]
            else:
                new_kwargs[x] = y
        data = f(*args, **new_kwargs) or {}
        return data
    return decorated_function


# GENERIC API Exposed
@fix_arg
@is_authorized(skip=[])
def schema_get(version, primary_schema, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].get_list(**kwargs)


@fix_arg
@is_authorized(skip=['user'])
def schema_post(version, primary_schema, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].create(**kwargs)


# ID Specific API Exposed
@fix_arg
@is_authorized(skip=[])
def schema_id_get(version, primary_schema, _id, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].get_id(_id=_id, **kwargs)


@fix_arg
@is_authorized(skip=[])
def schema_id_put(version, primary_schema, _id, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].edit_id(_id=_id, **kwargs)


@fix_arg
@is_authorized(skip=[])
def schema_id_delete(version, primary_schema, _id, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].delete_id(_id=_id, **kwargs)


# ID, FIELD Specific API Exposed
@fix_arg
@is_authorized(skip=[])
def schema_id_field_get(version, primary_schema, _id, field, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].get_id_field(_id=_id,
                                                                  field=field, **kwargs)


@fix_arg
@is_authorized(skip=[])
def schema_id_field_post(version, primary_schema, _id, field, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].post_field(_id=_id,
                                                                field=field, **kwargs)


@fix_arg
@is_authorized(skip=[])
def schema_id_field_put(version, primary_schema, _id, field, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].patch_field(_id=_id,
                                                                 field=field, **kwargs)


@fix_arg
@is_authorized(skip=[])
def schema_id_field_delete(version, primary_schema, _id, field, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].delete_field_value(_id=_id,
                                                                        field=field, **kwargs)


# Special Request
@fix_arg
@is_authorized(skip=[])
def schema_special_post_request(version, primary_schema, request_type, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].special_post_request(request_type, **kwargs)


@fix_arg
@is_authorized(skip=[])
def schema_special_get_request(version, primary_schema, request_type, **kwargs):
    return REGISTERED_ROUTE[version][primary_schema].schema_special_get_request(
        request_type, **kwargs)
