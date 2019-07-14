"""

Global Decorators

"""
from functools import wraps
from kernel import app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
from kernel.utils import CustomException, Codes, set_query_parameter
from kernel.models.db_obj import User


def rjsonify(data, total=0, flush_cache=False, load_more=False, next_url={}, **kwargs):
    if total > 50:
        total = 50
    res = {'data': data,
           'total': total,
           'flush_cache': flush_cache,
           "load_more": load_more,
           }
    if next_url:
        res['next_url'] = handle_next_url(next_url)
    return res


GEN_TOKEN = URLSafeTimedSerializer(app.config['TOKEN_GEN_SEC_KEY'],
                                   salt=app.config['TOKEN_GEN_SEC_SALT_KEY'])


def generate_refresh_token(email, _id):
    REF_TOKEN = URLSafeTimedSerializer(str(email), salt=app.config['REF_SECRET_KEY'])
    return REF_TOKEN.dumps({'_id': _id, 'email': email})


def tokenize(f):
    """
    is_authorized decorator check for user authorization
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Attach Token in Request
        data = f(*args, **kwargs) or {}
        if data.get('data') and data['data'].get('_id'):
            data['data']['token'] = GEN_TOKEN.dumps({'_id': data['data']['_id']})
            data['data']['refresh_token'] = generate_refresh_token(data['data']['email'], data['data']['_id'])
        return data
    return decorated_function


def handle_next_url(params, url = "?"):
    for k,v in params.iteritems():
        if isinstance(v, list):
            for _v in v:
                if isinstance(_v,datetime):
                    _v = datetime_to_epoch(_v)
                url = set_query_parameter(url, k, _v)
        else:
            if isinstance(v,datetime):
                v = datetime_to_epoch(v)
            url = set_query_parameter(url, k, v)
    return url


EPOCH = datetime.utcfromtimestamp(0)


def datetime_to_epoch(obj):
    try:
        if isinstance(obj, datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
            delta = obj - EPOCH
            millis = int(delta.total_seconds()*1000)
            return millis
    except TypeError:
        pass


def signature(params=[]):
    """
    Signature decorator is to check for required params
    Generate appropriate CustomException
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for param in params:
                if param not in kwargs:
                    raise CustomException('{} is a required parameter'.format(
                        param), Codes.NULL_PARAM)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def is_authorized(skip=[]):
    """
    Signature decorator is to check for required params
    Generate appropriate CustomException
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            kwargs['current_user'] = None
            if not kwargs['primary_schema'] in skip:
                token = kwargs.get('token')
                if token:
                    try:
                        user_id = GEN_TOKEN.loads(token, max_age=21000000)
                        user_default_fields = dict(User._default_fields_.items())
                        _user = User.get(user_id, fields=user_default_fields)
                        kwargs['current_user'] = _user.get(user_id, fields=user_default_fields).get_data()
                    except Exception as e:
                        print(e)
                        raise CustomException('Token Expired', 401)
                else:
                    raise CustomException('Pass token to authorize your request', 401)
            kwargs['skip'], kwargs['limit'] = validate_pagination(**kwargs)
            data = f(*args, **kwargs)
            return data
        return decorated_function
    return decorator


def get_max_skip(**kwargs):
    return app.config.get('MAX_SKIP', {}).get(kwargs.get('primary_schema', 'default'), {}).get(kwargs.get('request_type', 'default'), 260)


def validate_pagination(**kwargs):
    """
    Check Pagination values skip and limit and validate with global settings
    """
    primary_schema = kwargs.get('primary_schema') or 'default'
    pagination = app.config['PAGINATION'].get(primary_schema, app.config['PAGINATION'].get('default'))

    kwargs['skip'] = int(kwargs.get('skip') or pagination['skip'])
    kwargs['limit'] = int(kwargs.get('limit') or pagination['limit'])
    if pagination.get('max_skip') and kwargs['skip'] > pagination['max_skip']:
        raise CustomException("You are not allowed to View More.")
    if pagination.get('max_limit') and kwargs['limit'] > pagination['max_limit']:
        kwargs['limit'] = pagination['max_limit']
    return kwargs['skip'], kwargs['limit']
