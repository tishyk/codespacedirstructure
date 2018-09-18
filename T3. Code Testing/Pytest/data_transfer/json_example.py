"""JavaScript Object Notation"""

import json
import pprint

employee_string = """
{
    "people": [
        {
        "name":"John Smith",
         "phone":"380637892057",
         "emails":"John.Smith@email.com",
         "has_license":false
         },
        {
        "name":"Anna Smith",
             "phone":"380987898016",
             "emails":null,
             "has_license":true
        }
    ]
}
"""

data = json.loads(employee_string)

for person in data:
    print(person['phone'])
print(type(data))
#pprint.pprint(data)