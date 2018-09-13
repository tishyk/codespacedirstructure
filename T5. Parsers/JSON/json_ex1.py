import json

# JavaScript Object Notation was inspired by a subset of the
# JavaScript programming language dealing with object literal syntax.

# JSON supports primitive types, like strings and numbers, as well as nested lists and objects.
JSON_DATA = """{
    "firstName": "Jane",
    "lastName": "Doe",
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": [
        {
            "firstName": "Alice",
            "age": 6
        },
        {
            "firstName": "Bob",
            "age": 8
        }
    ]
}"""

"""
Python	            JSON
dict	            object
list, tuple 	    array
str	                string
int, long, float	number
True	            true
False	            false
None	            null
"""

# Imagine you’re working with a Python object in memory that looks a little something like this:

data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}

with open("data_file.json", "w") as write_file:
    # dump() takes two positional arguments:
    #  (1) the data object to be serialized, and
    # (2) the file-like object to which the bytes will be written
    json.dump(data, write_file)

# Serialize in a one
json_string = json.dumps(JSON_DATA)
print(json_string, end="-"*20)
print(json.dumps(JSON_DATA, indent=4))


# Deserializing JSON
blackjack_hand = (8, "Q")
encoded_hand = json.dumps(blackjack_hand)
decoded_hand = json.loads(encoded_hand)

blackjack_hand == decoded_hand          # --> False
type(blackjack_hand)                    # ---> <class 'tuple'>
type(decoded_hand)                      # --> <class 'list'>
blackjack_hand == tuple(decoded_hand)   # --> True


with open("data_file.json", "r") as read_file:
    # read from a file object( file/socket/stream/PIPE)
    data = json.load(read_file)
# In most cases, the root object will be a dict or a list


