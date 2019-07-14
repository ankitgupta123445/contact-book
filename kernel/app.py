"""

Backend APP Initialization

"""
from datetime import datetime
from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS
from flask.globals import request

PROJECT_NAME = "BackendAPI"

app = Flask(PROJECT_NAME)

app.config.from_object('kernel.settings')
cors = CORS(app)
EPOCH = datetime.utcfromtimestamp(0)


class CustomJSONEncoder(JSONEncoder):
    """
    Encodes date times as unix timestamps.
    """

    def _get_api_version(self):
        """
        api versions: v1
        """
        try:
            return request.view_args.get('version')
        except Exception as e:
            print(e)
            return None

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                delta = obj - EPOCH
                if self._get_api_version() in ["v1", None]:
                    millis = int(delta.total_seconds())
                else:
                    millis = int(delta.total_seconds() * 1000)
                return millis

            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder
