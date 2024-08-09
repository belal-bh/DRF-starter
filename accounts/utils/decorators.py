from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect


def unauthenticated_user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # get all groups of a user
            # user_groups = None
            # if request.user.groups.exists():
            #     user_groups = request.user.groups.all()

            # # verify user is allowed and return
            # for user_group in user_groups:
            #     if user_group.name in allowed_roles:
            #         return view_func(request, *args, **kwargs)

            print(f"groups:{request.user.groups.all()}")
            if request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)

            # that means user is not allowed
            return HttpResponseForbidden()
        return wrapper_func
    return decorator
