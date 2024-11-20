from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
#   path('signup/',
#          views.SignUpView.as_view(),
#          name='signup'),
    path('signup/', views.SignUpView.as_view(template_name="accounts/signup.html"), name='signup'),

    path('signup_success/',
         views.SignUpSuccessView.as_view(),
         name='signup_success'),
             
    path('login/',
         views.LoginView,
         name='login'
         ),

    path('logout/',
         auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout'
         ),
         
    path('',
         views.IndexView.as_view(template_name='accounts/index.html'),
         name='index')
]