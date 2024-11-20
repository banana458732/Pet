from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            return response
        login_url = reverse('accounts:login')
        allowed_paths = [
            reverse('accounts:signup'),
            reverse('accounts:signup_confirm'),
            reverse('accounts:signup_success'),
            reverse('accounts:logout'),
            reverse('top'),

            login_url,
        ]
        if request.path not in allowed_paths:
            return HttpResponseRedirect(login_url)
        
        return response