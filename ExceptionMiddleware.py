from sys        import exc_info
from traceback  import format_tb

class AnExceptionMiddleware( object ):
    def __init__( self, app ):
        super( AnExceptionMiddleware, self ).__init__()
        self.app = app

    def __call__( self, environ, start_response ):
        appiter = None
        try:
            appiter = self.app( environ, start_response )
            for item in appiter:
                yield item
        except:
            e_type, e_value, tb = exc_info()
            traceback = [ "Traceback (most recent call last):" ]
            traceback += format_tb( tb )
            traceback.append( "%s: %s" % ( e_type.__name__, e_value ) )

            try:
                start_response(
                    "500 INTERNAL SERVER ERROR",
                    [ ( "Content-Type", "text/plain" ) ]
                )
            except:
                pass
            yield "\n".join( traceback )
        if hasattr( appiter, "close" ):
            appiter.close()
