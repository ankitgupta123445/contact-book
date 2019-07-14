"""

Expose API Routes Here

"""

from kernel.api.v1.user import UserAPI
from kernel.api.v1.contact import ContactAPI


REGISTERED_ROUTE = {
    "v1": {
        'user': UserAPI(),
        'contact': ContactAPI()
    }
}
