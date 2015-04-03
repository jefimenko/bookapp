import re
from bookdb import BookDB

BOOKS = BookDB()

LIST_TEMPLATE = "<p><a href=\"/book/{id}\">{title}</a></p>"

INFO_TEMPLATE = "<div><p>Title: {title}</p><p>Author: {author}</p><p>Publisher: {publisher}</p><p>ISBN: {isbn}</p></div><div><a href=\"/\">back</a></div>"

def resolve_path(path_info):
    urls = [(r'^$', books),
            (r'^book/(id[\d]+)$', book)]
    clean_path = path_info.lstrip('/')
    for regex, function in urls:
        match = re.match(regex, clean_path)
        if match is None:
            continue
        args = match.groups([])
        return function, args
    raise NameError

def book(book_id):
    book = BOOKS.title_info(book_id)
    return INFO_TEMPLATE.format(**book)

def books():
    """
    Return html of hyperlinked book titles.
    """
    book_list = []
    for book in BOOKS.titles():
        book_list.append(LIST_TEMPLATE.format(id=book['id'], title=book['title']))
    book_list = '\n'.join(book_list)
    return '<div>{books}</div>'.format(books=book_list)

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except KeyboardInterrupt:
        body = ''
        status = ''
        quit()
    except NameError:
        status = "404 Not Found"
        body = "<h1>You failed</h1>"
    except exception:
        status = "500 Internal Server Error"
        body = "<h1>We failed</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()