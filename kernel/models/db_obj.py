from .base import BaseResource
from .db_schema import SCHEMAS


class User(BaseResource):
    """
      User Object mapped with users collection.
    """
    _coll_name_ = 'user'
    _schema_ = SCHEMAS['user']["schema"]
    _reserve_fields_ = SCHEMAS['user']["reserve_fields"]
    _default_fields_ = SCHEMAS['user']['default_fields']
    searchable_fields = SCHEMAS['user']['searchable_fields']
    search_mapping = SCHEMAS['user']['search_mapping']

    def __init__(self, arg):
        inp_args = arg if arg is not None else {}
        super(User, self).__init__(User._coll_name_, inp_args)


class Contact(BaseResource):
    """
      Contact Object mapped with case collection.
    """
    _coll_name_ = 'contact'
    _schema_ = SCHEMAS['contact']["schema"]
    _reserve_fields_ = SCHEMAS['contact']["reserve_fields"]
    _default_fields_ = SCHEMAS['contact']['default_fields']
    searchable_fields = SCHEMAS['contact']['searchable_fields']
    search_mapping = SCHEMAS['contact']['search_mapping']

    def __init__(self, arg):
        inp_args = arg if arg is not None else {}
        super(Contact, self).__init__(Contact._coll_name_, inp_args)


class TokenExpire(BaseResource):
    _coll_name_ = "token_expire"
    _schema_ = SCHEMAS['token_expire']['schema']
    _reserve_fields_ = SCHEMAS['token_expire']["reserve_fields"]
    _default_fields_ = SCHEMAS['token_expire']['default_fields']
    searchable_fields = SCHEMAS['token_expire']['searchable_fields']
    search_mapping = SCHEMAS['token_expire']['search_mapping']

    def __init__(self, arg):
        inp_args = arg if arg is not None else {}
        super(TokenExpire, self).__init__(TokenExpire._coll_name_, inp_args)
