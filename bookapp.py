import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book = DB.title_info(book_id)
    result = "<h1>Title: %s</h1>" % book.get('title')
    result += "<h3>Publisher: %s</h3>" % book.get('publisher')
    result += "<h3>Author: %s</h3>" % book.get('author')
    return result

def books():
    return "<h1>a list of books</h1>"

def resolve_path(path_info):
    kwargs = {}
    path_string = path_info.split('/')
    if path_info == '/':
        return books, kwargs
    else:
        kwargs = {'book_id': path_string[-1]}
        return book, kwargs

def application(environ, start_response):    
    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        resp, kwargs = resolve_path(path)
        body = resp(**kwargs)
        status = "200 OK"
    except NameError:
        status = "404 URL Not found"
        
        
    start_response(status, headers)
    return resp(**kwargs)

#   return ["<h1>No Progress Yet</h1>", ]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
