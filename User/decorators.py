# decorators for role Authentication
from rest_framework.response import Response


# Head master decoration to check user role is Head Master
def headMaster_role(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.role != 'HM':
            # raise Http404

            return Response({'EError': '{}'.format(request.user.role)})
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

# Teacher decoration to check user role is Teacher
def teacher_role(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.role != 'T':
            # raise Http404
            return Response({'EError': 'not authorized'})
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


# Student decoration to check user role is Student
def student_role(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.role != 'S':
            # raise Http404
            return Response({'EError': 'not authorized'})
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


# Parent decoration to check user role is Parent
def parent_role(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.role != 'P':
            # raise Http404
            return Response({'EError': 'not authorized'})
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func




