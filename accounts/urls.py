from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MyPageView, complete_contract, RedirectTemporaryPetView

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
          views.LogoutView.as_view(),
          name='logout'
          ),

     path('',
          views.IndexView.as_view(template_name='accounts/index.html'),
          name='index'),
     path('mypage/', MyPageView.as_view(), name='my_page'),  # 'mypage'ではなく'my_page'を使用
     path('contract/complete/', complete_contract, name='complete_contract'),
     path('temporary-pet/', RedirectTemporaryPetView.as_view(), name='temporary_pet'),
     path('change_profile_image/', views.change_profile_image, name='change_profile_image'),  # 追加
]
