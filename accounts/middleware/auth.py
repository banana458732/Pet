from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        rp = request.path
        if rp != '/accounts/login/' and not request.user.is_authenticated:
            if rp == '/accounts/signup/':
                return response
            elif rp == '/accounts/signup_confirm':
                return response
            elif rp == 'accounts/signup_success':
                return response
            elif rp == 'accounts/logout':
                return response
            return HttpResponseRedirect('/accounts/login/')
        return response