"""

Global Request Response Parser

"""

from flask import request, jsonify


def request_parser():
    """

    Request Parser will parse args and kwargs from request object

    """
    try:
        if request.method == "GET":
            return request.args
        elif request.method == "POST" or request.method == "PUT":
            args = request.json or request.form
            return args
        elif request.method == "DELETE":
            args = request.args
            if request.get_json(silent=True):
                request.json.update(dict(request.args))
                return request.json
            return args
        else:
            return request.args
    except Exception as e:
        print(e)
        return {}


def response_parser(data={}, response=None):
    """

    Response Handler will convert standard output format to desired format
    Currently JSON is standard output format

    """
    if data:
        return jsonify(status='success', data=data)
    elif response:
        return jsonify(response)
    else:
        return jsonify(status='success', data=data)
