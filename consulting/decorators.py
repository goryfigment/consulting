import json
from django.core.exceptions import PermissionDenied


def login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            print 'User not login'
            raise PermissionDenied('User not login.')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def data_required(required_data, request_type):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            if request_type == "POST":
                request.POST = request.POST.dict()
                query_request = request.POST
            elif request_type == "GET":
                request.GET = request.GET.dict()
                query_request = request.GET
            elif request_type == "FILES":
                query_request = request.FILES
            else:
                query_request = json.loads(request.body)
                request.BODY = query_request

            for data in required_data:
                if data not in query_request:

                    if request_type == 'FILES':
                        if data in request.POST:
                            continue

                    print data + ' does not exist!'
                    raise PermissionDenied(data + ' does not exist!')
            return function(request, *args, **kwargs)
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return decorator
