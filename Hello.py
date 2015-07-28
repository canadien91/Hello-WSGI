
import re
from cgi                    import escape
from ExceptionMiddleware    import AnExceptionMiddleware

def Index( environ, start_response ):
    start_response( "200 OK", [ ( "Content-Type", "text/html" ) ] )
    return [ """
    This is the Hello World application
    """ ]

def Hello( environ, start_response ):
    args = environ["myapp.url_args"]
    if args:
        subject = escape( args[ 0 ] )
    else:
        subject = "World"
    start_response( "200 OK", [ ( "Content-Type", "text/html" ) ] )
    return [ "Hello %(subject)s" % { "subject": subject } ]

def NotFound( environ, start_response ):
    start_response( "404 NOT FOUND", [ ( "Content-Type", "text/plain" ) ] )
    return ["Not Found"]

urls = [
    ( r"^$", Index ),
    ( r"hello/?$", Hello ),
    ( r"hello/(.+)$", Hello ),
]

def Application( environ, start_response ):
    path = environ.get( "PATH_INFO", "" ).lstrip( "/" )
    for regex, callback in urls:
        match = re.search( regex, path )
        if match is not None:
            environ["myapp.url_args"] = match.groups()
            return callback( environ, start_response )
    return NotFound( environ, start_response )

Application = AnExceptionMiddleware( Application )

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server( "localhost", 8000, Application )
    srv.serve_forever()
