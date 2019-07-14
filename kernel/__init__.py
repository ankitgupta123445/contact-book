from kernel.app import app

from .urls import api as api_blueprint

ALL_BLUEPRINTS = [
    [api_blueprint, "/"],
]
for bp in ALL_BLUEPRINTS:
    app.register_blueprint(bp[0], url_prefix=bp[1])


