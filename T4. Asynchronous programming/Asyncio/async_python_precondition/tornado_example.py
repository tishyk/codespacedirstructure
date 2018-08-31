"""
To explain the code a little, the very last line is calling
a tornado method called AsyncHTTPClient.fetch which fetches a url in a non-blocking way.
This method essentially executes and returns immediately allowing the program to do other things,
while waiting on the network call. Because the next line is reached before the url has been hit,
it is not possible to get a return object from the method.
The solution to this problem is that instead of the fetch method returning an object,
it calls a function with the result, or a callback.
The callback in this example is handle_response.
"""


import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
urls = ['http://www.google.com', 'http://www.yandex.ru', 'http://www.python.org']

def handle_response(response):
    if response.error:
        """
        This is required because it is not possible to raise an exception. 
        If an exception was raised, it would not be handled by the proper section of code, due to the event loop.
        When fetch is executed, it starts the http call, then puts handling the response on the event loop.
        By the time we notice our error, the call stack would only be the event loop and this function,
        with none of our code to handle the exception. 
        So any exceptions thrown in the callback will break the event loop and the program. 
        Therefore all errors have to be passed as objects rather than raised.
        This means if you forget to check for errors, your errors will be swallowed. 
        """
        print("Error:", response.error)
    else:
        url = response.request.url
        data = response.body
        print('{}: {} bytes: {}'.format(url, len(data), data))

http_client = AsyncHTTPClient()
for url in urls:
    http_client.fetch(url, handle_response)

tornado.ioloop.IOLoop.instance().start()