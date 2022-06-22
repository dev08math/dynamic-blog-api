from asyncio.base_subprocess import ReadSubprocessPipeProto
from cgitb import handler
from logging import handlers
from urllib import response
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)    # getting the standard error response first

    def _handle_generic_error(exc, context, response):
        status_code = response.status_code        # customising the status code
        response.data = {"statuc_code" : status_code, "error" : response.data}   # custom response
        return response

    def _handle_not_found_error(exc, context, response):
        view  = context.get("view", None)
        if view and hasattr(view, "queryset") and view.queryset is not None:
            status_code  = response.status_code
            error_key = view.queryset.model._meta.verbose_name
            response.data  = {
                "status_code" : status_code,
                "errors" : {error_key : response.data["detail"]},
            }
        else:
            response = _handle_generic_error(exc, context, response)
        return response

    handlers = {
        'ValidationError' : _handle_generic_error,
        'NotFound' : _handle_not_found_error
    }

    exception_class  = exc.__class__.__name__     # gives the error which is raised 

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response                               # let django handle the exception the exception if its not in handlers


    
