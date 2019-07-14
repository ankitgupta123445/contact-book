"""
API Version : V1
User API

"""

import hashlib
from six import string_types
from kernel.api.base import BaseHandler
from kernel.util.decorators import (signature, tokenize, rjsonify)
from kernel.models.db_obj import User
from kernel.utils import CustomException, Codes
from kernel.utils import suppress
from kernel.app import app

"""
UserAPI is an implementation of BaseHandler to expose /user api.
"""


class UserAPI(BaseHandler):
    """
    API for user manipulation.
    General pagination:
        skip: Skips over the first `skip` number of users.
        limit: Provides a maximum of `limit` number of users.
    """
    def _get_detail_fields(self):
        return {'email': 1, **dict(User._default_fields_.items())}

    def get_list(self, is_editor=True, skip=0, limit=25, first_name=None,
                 last_name=None, email=None, _id=None, **kwargs):
        """Provides list of users.

         Searches by `email`, `first_name` and `last_name`.
        """
        _query = {}

        _fields = dict(User._default_fields_.items())

        if first_name:
            _query['first_name'] = first_name

        if last_name:
            _query['last_name'] = last_name

        if email:
            _query['email'] = email

        if _id:
            _query['_id'] = _id
        _users = User.get_all(_query,
                              fields=_fields,
                              skip=skip,
                              limit=limit,
                              sort_by=[('_id', -1)])
        if _users:
            return rjsonify([user.get_data() for user in _users])
        return rjsonify([])

    @signature(params=['first_name', 'email', 'password'])
    @tokenize
    def create(self, first_name, email, password, last_name='', **kwargs):
        """
        Registers new user
        :param first_name:
        :param email:
        :param password:
        :param last_name:
        :param kwargs:
        :return:
        Required : email, name, password
        """
        _fields = self._get_detail_fields()
        with suppress(Exception):
            email = email.lower()

        _user = User.get({'email': email}, fields=['_id'])
        password = self.__salt_hashed_password(email, password)
        if _user:
            _user_data = _user.get_data()
            _user_id = _user_data['_id']
            _user_valid = User.get({'email': email, 'password': password}, fields=['_id'])
            if not _user_valid:
                raise CustomException('Sorry, it looks like {} belongs to an existing account.'.format(email) +
                                      "Please try logging in", Codes.CONFLICT)

        else:
            new_user = {'first_name': first_name,
                        'last_name': last_name,
                        'email':  email,
                        'password': password,
                        }
            try:
                _user = User(new_user)
                _user_id = _user.insert()
            except Exception as e:
                raise CustomException(str(e), Codes.INVALID_PARAM)
        user_data = User.get({'_id': _user_id}, fields=_fields).get_data()
        return rjsonify(user_data)

    """ID Specific APIs"""
    def get_id(self, _id, **kwargs):
        """
        To get single record for a given _id.

        The user himself is allowed to see his various scores and
        contact information.
        """
        if _id == kwargs['current_user']['_id']:
            _fields = self._get_detail_fields()
        else:
            _fields = User._default_fields_
        _user = User.get({'_id': _id}, fields=_fields)
        if not _user:
            return rjsonify({})
        return rjsonify(_user.get_data())

    def edit_id(self, _id, **kwargs):
        """Put request, to update or replace record for given _id and data"""
        pass

    def delete_id(self, _id, **kwargs):
        """delete request to delete _id record"""
        pass

    """ID and FIELD Specific API"""

    def get_id_field(self, _id, field, skip=0, limit=25, **kwargs):
        """
        Record level GET endpoint..
        """
        pass

    def post_field(self, _id, field, **kwargs):
        """Record level POST endpoints."""
        pass

    def patch_field(self, _id, field, **kwargs):
        """Update field data for a given _id"""
        pass

    def delete_field_value(self, _id, field, **kwargs):
        """Request to delete an item from an array field or
        unset other field data"""
        pass

    """SPECIAL Request API"""

    def special_post_request(self, request_type, **kwargs):
        """Schema level POST endpoint."""
        pass

    def schema_special_get_request(self, request_type, **kwargs):
        """
        Generic base method which provides a capabilities for special get
        request other than get_all
        """
        pass

    """HELPER Functions"""

    def __salt_hashed_password(self, salt, password):
        """Hash PASSWORD with USER Salt And SYSTEM SALT"""
        if not isinstance(password, string_types):
            password = str(password)
        return hashlib.sha512((salt+password + app.config['APP_PWD_SALT']).encode('utf-8')).hexdigest()
