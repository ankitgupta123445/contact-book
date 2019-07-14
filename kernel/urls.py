"""

Contact Book Backend API URL

"""
from urllib.parse import unquote
from .router import APP_ROUTER
from kernel import app
from .utils import CustomException, Codes
from flask import Blueprint, request, jsonify, url_for
from kernel.util.parser import request_parser, response_parser

api = Blueprint('api', __name__)


@app.errorhandler(CustomException)
def custom_exception(error):
    """
    TODO : Create Error PAYLOAD here From Request
    CustomException Exception API to return CustomException response
    """
    response = jsonify(error._repr())
    return response


@app.errorhandler(Exception)
def exception_handler():
    # Need to Add Error Filtering. Right now masking all Exception.
    return jsonify(status="failed", error_msg="Internal Error Occurred. " +
                                              "We Broke Something, our experts will be fixing it up Soon !!",
                   code=Codes.INTERNAL_ERROR)


@api.route('/')
def index():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        url = url_for(rule.endpoint, **options)
        line = unquote("{}".format(url))
        output.append(line)
    return response_parser(data=output)


# GENERIC API Exposed
@api.route('<version>/<primary_schema>', methods=['GET', 'POST'])
def generic_schema_api(version, primary_schema):
    if request.method == "GET":
        data = APP_ROUTER[version].schema_get(
            version=version,
            primary_schema=primary_schema,
            **request_parser())
    elif request.method == "POST":
        data = APP_ROUTER[version].schema_post(
            version=version,
            primary_schema=primary_schema,
            **request_parser())
    else:
        raise CustomException('Invalid Request', Codes.NOT_ALLOWED)
    return response_parser(data=data)


# ID Specific API Exposed
@api.route('<version>/<primary_schema>/<_id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def generic_primary_id_api(version, primary_schema, _id):
    if request.method == "GET":
        data = APP_ROUTER[version].schema_id_get(
            version=version,
            primary_schema=primary_schema,
            _id=_id, **request_parser())
    elif request.method == "PUT":
        data = APP_ROUTER[version].schema_id_put(
            version=version,
            primary_schema=primary_schema,
            _id=_id, **request_parser())
    elif request.method == "DELETE":
        data = APP_ROUTER[version].schema_id_delete(
            version=version,
            primary_schema=primary_schema,
            _id=_id, **request_parser())
    else:
        raise CustomException('Invalid Request', Codes.NOT_ALLOWED)
    return response_parser(data=data)


# ID, FIELD Specific API Exposed
@api.route('<version>/<primary_schema>/<_id>/<field>',
           methods=['GET', 'POST', 'PUT', 'DELETE'])
def generic_id_field_api(version, primary_schema, _id, field):
    if request.method == "GET":
        data = APP_ROUTER[version].schema_id_field_get(
            version=version,
            primary_schema=primary_schema,
            _id=_id, field=field, **request_parser())
    elif request.method == "POST":
        data = APP_ROUTER[version].schema_id_field_post(
            version=version,
            primary_schema=primary_schema,
            _id=_id, field=field, **request_parser())
    elif request.method == "PUT":
        data = APP_ROUTER[version].schema_id_field_put(
            version=version,
            primary_schema=primary_schema,
            _id=_id, field=field, **request_parser())
    elif request.method == "DELETE":
        data = APP_ROUTER[version].schema_id_field_delete(
            version=version,
            primary_schema=primary_schema,
            _id=_id, field=field, **request_parser())
    else:
        raise CustomException('Invalid Request', Codes.NOT_ALLOWED)
    return response_parser(data=data)


# SPECIAL Request
@api.route('<version>/<primary_schema>/i/<request_type>', methods=['POST', 'GET'])
def generic_post_request_api(version, primary_schema, request_type):
    if request.method == 'POST':
        data = APP_ROUTER[version].schema_special_post_request(
            version=version,
            primary_schema=primary_schema,
            request_type=request_type, **request_parser())
    elif request.method == 'GET':
        data = APP_ROUTER[version].schema_special_get_request(
            version=version,
            primary_schema=primary_schema,
            request_type=request_type,
            **request_parser())
    return response_parser(data=data)


@api.route('<version>/user', methods=['GET', 'POST'])
def user_schema_api(version):
    if request.method == "GET":
        data = APP_ROUTER[version].schema_get(
            version=version,
            primary_schema="user",
            **request_parser())
    elif request.method == "POST":
        data = APP_ROUTER[version].schema_post(
            version=version,
            primary_schema="user",
            **request_parser())
    else:
        raise CustomException('Invalid Request', Codes.NOT_ALLOWED)
    return response_parser(data=data)


@api.route('<version>/login', methods=['POST'])
def login(version):
    data = APP_ROUTER[version].login(version=version, **request_parser())
    return response_parser(data=data)


@api.route('<version>/forgot_password', methods=['POST'])
def forgot_password(version):
    data = APP_ROUTER[version].forgot_password(version=version, **request_parser())
    return response_parser(data=data)


@api.route('<version>/reset_password', methods=['POST', 'GET'])
def reset_password(version):
    data = APP_ROUTER[version].reset_password(version=version,
                                              dr_action="attach_token", **request_parser())
    return response_parser(data=data)


@api.route('<version>/token', methods=['POST'])
def get_token(version):
    data = APP_ROUTER[version].token(version=version,
                                     dr_action="handle_ref_token", **request_parser())
    return response_parser(data=data)


@api.route('<version>/unsubscribe', methods=['POST'])
def unsubscribe(version):
    data = APP_ROUTER[version].unsubscribe(version=version, **request_parser())
    return response_parser(data=data)


@app.errorhandler(404)
def page_not_found(error):
    return response_parser(response={"status": "404", "error_msg": "API Not found."})


@app.errorhandler(405)
def page_not_found(error):
    return response_parser(response={"status": "405", "error_msg": "API Not found."})
