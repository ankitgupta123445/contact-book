"""

Abstract Base class for API Handler interface
All API Handlers to inherit from this base class

"""
from abc import ABCMeta, abstractmethod


class BaseHandler:
    __metaclass__ = ABCMeta

    """
    Generic APIs
    """

    @abstractmethod
    def get_list(**kwargs):
        """
        Generic base method which provides a capabilities to get list of records
        """
        pass

    @abstractmethod
    def create(**kwargs):
        """
        Generic base method which provides a capabilities to create new record
        """
        pass

    """
    Record ID Specific APIs
    """

    @abstractmethod
    def get_id(_id, **kwargs):
        """
        Generic base method which provides a capabilities to get single
        record for a given _id
        """
        pass

    @abstractmethod
    def edit_id(_id, **kwargs):
        """
        Generic base method which provides a capabilities
        to update or replace record for given record _id and data
        """
        pass

    @abstractmethod
    def delete_id(_id, **kwargs):
        """
        Generic base method which provides a capabilities to
        delete record with given record _id
        """
        pass

    """
    ID and FIELD Specific API
    """

    @abstractmethod
    def get_id_field(_id, field, **kwargs):
        """ To get specific field data for a given _id """
        pass

    @abstractmethod
    def post_field(_id, field, **kwargs):
        """ TO support Field post request for a given _id """
        pass

    @abstractmethod
    def patch_field(_id, field, **kwargs):
        """
        Generic base method which provides a capabilities to Update
        field data for a given record _id
        """
        pass

    @abstractmethod
    def delete_field_value(_id, field, **kwargs):
        """
        Generic base method which provides a capabilities to delete
        an item from an array field or unset other field data
        for a given record _id
        """
        pass

    """
    SPECIAL Request
    """

    @abstractmethod
    def special_post_request(request_type, **kwargs):
        """
        Generic base method which provides a capabilities for special post
        request other than create without providing record _id
        """
        pass

    @abstractmethod
    def schema_special_get_request(request_type, **kwargs):
        """
        Generic base method which provides a capabilities for special get
        request other than get_all
        """
        pass
