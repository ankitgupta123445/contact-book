"""

Expose API Routes Here

"""

from kernel.api.v1.user import UserAPI


REGISTERED_ROUTE = {
    "v1": {
        'user': UserAPI()
    }
}
