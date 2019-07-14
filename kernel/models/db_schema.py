"""

Database Schema


reserve_fields      : Restricted Field, Not allowed to retrieve field value from Database
hidden_fields       : Restricted Fields, Not allowed to edit via Edit field call System
                      generated fields can only be update by system
searchable_fields   : Fields indexed in Elastic Search for Search
required            : Required fields
default_fields      : default fields to retrieve from Database


"""

KNOWN_DOSE_TYPE = ["mobile"]

INTERNAL_FIELDS = {
    "is_deleted": {"type": "boolean"},
    "created_on": {"type": "datetime"},
    "last_updated": {"type": "datetime"},
    "_last_updated": {"type": "datetime"}
}


SCHEMAS = {
    "user": {
        "reserve_fields": ["password"],
        "hidden_fields": [],
        "default_fields": {"first_name": 1,
                           "last_name": 1,
                           },
        "searchable_fields": [],
        "search_mapping": {},
        "schema": {
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string",

                },
                "last_name": {
                    "type": "string"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                },
                "password": {
                    "type": "string"
                },
            },
            "required": ["first_name", "password", "email"]
        }
    },
    "contact": {
        "reserve_fields": [],
        "hidden_fields": [],
        "default_fields": {"first_name": 1,
                           "last_name": 1,
                           "email": 1,
                           "mobile": 1,
                           "created_on": 1,
                           "last_updated": 1
                           },
        "searchable_fields": [],
        "search_mapping": {},
        "schema": {
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string"
                },
                "last_name": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "mobile": {
                    "type": "string"
                },
                "created_on": {
                    "type": "datetime"
                },
                "last_updated": {
                    "type": "datetime"
                },
            },
            "required": ["first_name", "email"]
        }
    },
    "token_expire": {
        "reserve_fields": [],
        "hidden_fields": [],
        "default_fields": {
            "token": 1,
            "count": 1,
        },
        "searchable_fields": [],
        "search_mapping": {},
        "schema": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string"
                },
                "count": {
                    "type": "number"
                }
            },
            "required": []
        }
    }
}


