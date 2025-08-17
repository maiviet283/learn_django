from django.shortcuts import redirect
from functools import wraps


def login_required_session(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('customer_id'):
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper