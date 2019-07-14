# contact-book

_A suite of CRUD APIs for a contact book app_

_Each contact have a unique email address_ 

_APIs support adding/editing/deleting contacts_ 

_Allowed searching by name and email address_ 

_Search support pagination and returns 10 items by default per invocation_ 

_Unit tests and Integration tests for each functionality_

_Added basic authentication for the app._ 

_Environment variables or basic auth(for rest APIs)_


###### Steps to run

`./bin/setup-dependency.sh`

`python runserver.py`

`create user `

`API: <base_url>/v1/user`

###### Payload:
 
    {"first_name": "Jay",
    
    "last_name": "Prakash",
    
    "email":"jaymailbox2012@gmail.com",
    
    "password": "jp543672"}


1. Response will return auth_token 
2. Test CRUD contact using token as API Header