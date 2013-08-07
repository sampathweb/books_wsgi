import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    result = "<h1>Title: %s</h1>" % book.get('title')
    result += "<h3>Publisher: %s</h3>" % book.get('publisher')
    result += "<h3>Author: %s</h3>" % book.get('author')
    return result

def books():
    book_list = DB.titles()
    result = "<h1>a list of books</h1>\n"
    result += "<ul>\n"
    for book in book_list:
        result += "<li <a href=/book/%s>>%s</li>\n" % (book['id'], book['title'])
    result += "</ul>"
    return result


def resolve_path(path):
    urls = [(r'^$', books),
            (r'^book/(id[\d]+)$', book)]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        args = match.groups([])
        return func, args
    # we get here if no url matches
    raise NameError


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        import pdb;pdb.set_trace()
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
