import json
import requests

# Task: get data from a web server with request "https://jsonplaceholder.typicode.com/todos"

response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)


# practice https://github.com/tishyk/api_test_scripts/blob/master/github_api_testing.py