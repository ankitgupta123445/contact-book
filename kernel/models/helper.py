from schemas import schemas
from kernel.utils import CustomException, Codes
from db_obj import User

MODEL_SCHEMA_MAP = {
    'user': User
}


def get_field_data_type(schema_name, field):
    is_valid_field(schema_name, field)
    return schemas[schema_name]['schema']['properties'][field]['type']


def get_schema_keys(schema_name):
    """Return Only Non hidden_fields """
    return list(key for key in get_schema_keys_all(schema_name) if key not in schemas[schema_name]['hidden_fields'])


def get_schema_keys_all(schema_name):
    """return all keys including hidden_fields"""
    return schemas[schema_name]['schema']['properties'].keys()


def is_required_field(schema_name, field):
    field = field.split('.')[0]
    if field in schemas[schema_name]['schema']['required']:
        raise CustomException("Unable to Delete,field Is Required", Codes.INVALID_PARAM)
    is_valid_field(schema_name, field)
    return schemas[schema_name]['schema']['properties'][field]['type']


def is_valid_field(schema_name, field, hidden_fields=True):
    field = field.split('.')[0]
    if field not in schemas[schema_name]['schema']['properties'].keys():
        raise CustomException('Invalid field', Codes.INVALID_PARAM)
    if hidden_fields:
        is_hidden_field(schema_name, field)
    return schemas[schema_name]['schema']['properties'][field]['type']


def is_reserved_field(schema_name, field):
    field = field.split('.')[0]
    if field in schemas[schema_name]['reserve_fields']:
        raise CustomException('Invalid field', Codes.INVALID_PARAM)
    is_valid_field(schema_name, field, False)
    return schemas[schema_name]['schema']['properties'][field]['type']


def is_hidden_field(schema_name, field):
    field = field.split('.')[0]
    if field in schemas[schema_name]['hidden_fields']:
        raise CustomException('Invalid field', Codes.INVALID_PARAM)


def get_searchable_fields(schema_name):
    return schemas[schema_name]['searchable_fields']


def is_searchable_field(schema_name, field):
    field = field.split('.')[0]
    if field in schemas[schema_name]['searchable_fields']:
        return True
    else:
        return False
