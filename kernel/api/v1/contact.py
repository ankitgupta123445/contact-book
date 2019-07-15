from kernel.api.base import BaseHandler
from kernel.utils import CustomException, Codes
from kernel.util.decorators import signature, rjsonify
from kernel.models.db_obj import Contact


class ContactAPI(BaseHandler):
    def _get_detail_fields(self):
        return {
            'first_name': 1,
            'last_name'
            'email': 1,
            'mobile': 1,
        }

    def get_list(self, first_name='', last_name='', email='', skip=0, limit=25, **kwargs):
        """Provides list of contact.

         Searches by `email`, `first_name` and `last_name`.
        """
        _query = {}
        if first_name:
            _query['first_name'] = first_name

        if last_name:
            _query['last_name'] = last_name

        if email:
            _query['email'] = email
        _fields = dict(Contact._default_fields_.items())
        _contacts = Contact.get_all(_query,
                                    fields=_fields,
                                    skip=skip,
                                    limit=limit,
                                    sort_by=[('_id', -1)])
        if _contacts:
            return rjsonify([contact.get_data() for contact in _contacts])
        return rjsonify([])

    @signature(params=['first_name', 'email'])
    def create(self, first_name, email, last_name='', mobile='', **kwargs):
        """
        Contact Create:
            first_name  :string
            email       :string
        """

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "mobile": mobile,
        }
        _fields = self._get_detail_fields()
        _contact = Contact.get({'email': email}, fields=_fields)
        if _contact:
            raise CustomException('Sorry, it looks like {} belongs to an existing contact.'.format(email) +
                                  "Please try new email", Codes.CONFLICT)
        try:
            contact = Contact(data)
            contact_id = contact.insert()
        except Exception as e:
            raise CustomException(str(e), Codes.INVALID_PARAM)
        contact_data = Contact.get({'_id': contact_id})
        return rjsonify(contact_data.get_data())

    def get_id(self, _id, **kwargs):
        """
        To get single record for a given _id.
        """
        _fields = self._get_detail_fields()
        _contact = Contact.get({'_id': _id}, fields=_fields)
        if not _contact:
            return rjsonify({})
        return rjsonify(_contact.get_data())

    def edit_id(self, _id, **kwargs):
        contact = Contact.get({'_id': _id})
        if not contact:
            raise CustomException("Contact Not Found")
        contact_data = contact.get_data()

        _u = {}
        for key in ["first_name", "last_name", "email", "mobile"]:
            if kwargs.get(key):
                if kwargs[key] != contact_data.get(key):
                    ignore_last_update = False
                    if not _u.get('$set'):
                        _u['$set'] = {}
                    _u['$set'][key] = kwargs.get(key)
        try:
            contact.patch_update(_u, ignore_last_update=ignore_last_update)
        except Exception as e:
            raise CustomException("Error while updating Training Lesson : {}".format(e))
        return rjsonify(Contact.get({'_id': _id}).get_data())

    def delete_id(self, _id, **kwargs):
        """
        Delete record
        """
        contact = Contact.get({'_id': _id}, fields=['first_name', 'email'])
        if contact:
            contact.delete()
            try:
                contact.delete()
            except Exception as e:
                raise CustomException("Error while deleting Contact : {}".format(e))
        else:
            raise CustomException("_id not found", Codes.NOT_FOUND)
        return rjsonify({'_id': _id, 'is_deleted': True})

    def get_id_field(self, _id, field, **kwargs):
        pass

    def post_field(self, _id, field, **kwargs):
        pass

    def patch_field(self, _id, field, **kwargs):
        pass

    def delete_field_value(self, _id, field, **kwargs):
        pass

    def special_post_request(self, request_type, **kwargs):
        pass

    def schema_special_get_request(self, request_type, **kwargs):
        pass
